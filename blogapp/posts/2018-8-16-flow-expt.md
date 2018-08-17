---
layout: post
title: Flow Typing a JS Experiment Framework
date: 2018-8-16
---

Today a colleague and I were building out our frontend experiment framework. The idea was simple -- a static object, initialized on page load with a JS object containing a mapping of experiment names to cohorts, and a few convenience methods to see if the user was in a given cohort for an experiment. Easy enough, but we decided to take it a step further and use Flow to make sure of a few things:

1. All experiment names passed into our convenience functions are valid.
2. All cohort names are similarly valid.
3. Ensure that all requests to see if the user is in cohort `x` for experiment `y` are valid; in other words, that `x` is one of the cohorts registered for experiment `y`.
4. All of the above should be done statically by Flow.

This turned out to be surprisingly tough. The main issue we ran into is that it wasn't possible to type one argument based on another. In Flow-ish pseudocode, I wanted something like this:

	:::js
	/**
	 * Determine if the user is in cohort `experimentCohort`
	 * of experiment `experimentName`.
	 */
	function experimentInCohort(
		experimentName: ExperimentName,
		experimentCohort: ExperimentCohorts[ExperimentName],
	): boolean {...}

But of course, that's not remotely valid Flow! I'd have to think of something a little cleverer.

<!--more-->

An idiom I'd employed elsewhere in the codebase was use Flow's [disjoint union feature](https://flow.org/blog/2015/07/03/Disjoint-Unions/), which allows us to ensure that one piece of data is correctly typed based on some other data in the same object. That iteration of this project looked like this:

	:::js
	type Expt1 = {name: 'word_art_mode', cohort: 'status_quo' | 'enabled'};
	type Expt2 = {name: 'map_size', cohort: 'status_quo' | 'big' | 'hella_big'};

	type Experiment = Expt1 | Expt2;

	// this is piped to us from the backend as a generic map; parse it so Flow
	// can't see its contents statically and help our typechecking that way.
	const buckets = JSON.parse(`{
		"word_art_mode": "enabled",
		"map_size": "hella_big"
	}`);

	function experimentInCohort(experiment: Experiment): boolean {
		return buckets[experiment.name] === experiment.cohort;
	}

	// this is gucci
	experimentInCohort({name: 'word_art_mode', cohort: 'enabled'});
	// we caught a bad experiment name!
	experimentInCohort({name: 'drop_shadow_mode', cohort: 'enabled'});
	// we caught a bad cohort name!
	experimentInCohort({name: 'map_size', cohort: 'giganto'});
	// we caught a bad name/cohort pair!
	experimentInCohort({name: 'map_size', cohort: 'enabled'});

[Try it live](https://flow.org/try/#0C4TwDgpgBAogHmYBGKBeKBvAdgQwLYQBcUA5AO4D2ATgCYD6OVwdeFNEJANFAMYUAW1YMRIBnYDmABXUXQCOUiiSgAfUhFwAjADYQaJAL4BuAFChIsBMABMaTLgIi8OMHVEBLAF4dufQUxFxSRl5RWU1Ek13AHNw0n4IbW0cOijY4xMzcGh4SCp3AixgO1zkVUtEa1MTAHoaqGB+d1EoZqgwd0gaBoooGSgAMyoKPAaEqE0cHgBrDW6cFpwoaI0IfJ4oZzAjdsZRaHdi0V6AMW0KMlr6nhwsEiOIA+AWviKNZ6gg4HcbpJAoW7dBLaMBQChSKgNbI8BIzdxYaJjSRQMg4EAAOhMr3EEykMwgH3QACkAMoAeQAcuiwHsIAAKAAGGBMAEgAESUWgMJgsNgQNnENkaHA6PRszistlbNxefmC4HJVIxNkmAwMgCU1QGUiwPG+FCwUAgCDWBXeAEksABhARCOnGvJmorEXKmwrAdXETQUCi6W6YExQKBUAkQw2aPGzZ4AbQdbve6IcEAAumhUOg4-l3ei-EJTAZMnUxm02tE8Tx3CZM07gJabf5gHTsPgiKROfRGMxWOwuLxbQF1FpdPoDJqrijoDcpNF+MUlpNutX3VAkwBCKsmrMW639xvNxykGjDVyifg4GgXXk93y7kTC0UjsdFsiTnDT2cAibnvsNlct9dLtu9Z2vurYkNKHjeL2uYDiQ0QxLcwBKKOpjPq+75zl+3RJjUMHFDS7hUABm41nWu5NkmTguDKUE3g2d5DnohiakAA)!

And it works, with helpful Flow error messages to boot! But let's take a closer look at the API of `experimentInCohort`. Having to declare an object literal inline every time we want to check a cohort is a pain, but we've already established that Flow doesn't allow us to explicitly link two arguments' types together. But what if we did it implicitly, outside the function declaration?

	:::js
	// These are more concise now!
	type Expt1 = {word_art_mode: 'status_quo' | 'enabled'};
	type Expt2 = {map_size: 'status_quo' | 'big' | 'hella_big'};

	type Experiment = Expt1 | Expt2;

	// We have to use $Exact<> here to catch the "invalid experiment name" case
	type Buckets = $Exact<Expt1 & Expt2>;

	// this is piped to us from the backend as a generic map; parse it so Flow
	// can't see its contents statically and help our typechecking that way
	const buckets: Buckets = JSON.parse(`{
		"word_art_mode": "enabled",
		"map_size": "hella_big",
	}`);

	// Existential types are super useful here!
	function experimentInCohort(name: *, cohort: *): boolean {
		// Coerce the args into an object to typecheck them together
		const experiment: Experiment = {[name]: cohort};
		// Then continue just like before
		return buckets[name] === cohort;
	}

	// this is gucci
	experimentInCohort('word_art_mode', 'enabled');
	// we caught a bad experiment name!
	experimentInCohort('drop_shadow_mode', 'enabled');
	// we caught a bad cohort name!
	experimentInCohort('map_size', 'giganto');
	// we caught a bad name/cohort pair!
	experimentInCohort('map_size', 'enabled');

[Try it live](https://flow.org/try/#0PTAEBUAsFMGdtAQwE4ILYHtWgMYYHY4CW8o+GA7gIQBQALgJ4AOCAogB5N0CMoAvKADeFLABMA+ijrjMo6AC5QAclh1EdAK6xxARw0YloAD7Lo+RACMANtFFKAvgG56zNpzoAmfkLSIm42CIALwVlVXUtXX1DEyULIgBzGOUYKytEcXikpxoXFlAOFmQiNDM6b0KeYwL3D2caEFAAdQRIRAA3BDoMUC0EABIORBw6AB4APlAYbG7cdRxIUDoYUAAiInx2xCsiUVBoTmhi0vxy81LVufg8hAAhDRwAa2g6WG9B9mGxyt4AMhquB5xvVGssSKBwUwiCw9rMtKAAGbIDBoJYrCzDZ74PaIN6IUAJMxHIg4UC+JiOUBMFCkIjlWA9ABiVkoDTAOEQ+CU9OgCDpbzwpzKb3CdBJ2ysDCQ2Km0CsTFAGA0yCWrgW0CeGwSaPUoAoiAYNEFqlAFgez1einuTxebwEACkAMoAeQAcgA6anIeAACgABoIaKBg2sRMgJFIZBg5KtFKszJYbKJVgAaIMh1bkgLBaCxtapdKZRKpmj2P0AShBYA4JDoZSI21VLDx2FgGiKvXgCI0VllqFo3cIYoI+0OxzKAEl8ABhDCQLB0H3nUIAKhTuDnC8UK-LigsGAwNk5QnTwcas6OOC6KxQCTeG1mx40+D6ewwFgAVhryo-YPBkD+aowJq+AJKeG74CaBxFCUZSKIUxInOUAiCAA2suAC6ih4POAE5CGoCNFAZgQWKL4IB+WjlDszymtACJYNA4GoJoyD4Ka5q2uhiClBh-B8AIOELs49i5KCkDguCCQPMQNDQYhk4zpuAE+koYYRgBUZyEo65KAm1i2EolZsnqCAchoCSQOU+IYns8njqcZA8dAtD2bBpxTrOuGLkoojIv4sBtKIlBadAOmmOYBl2MZjQUGZiAWVZSCmogexCQBTmlK5Y7uXQnnKT5WaBCE4VKAkiSct0RnOLF8WJdZKV7MuwDpeU1JEMg2UwUh+XeapRU5qV+lJtVQA)!

Much better. The experiment types are more concise, as is the `experimentInCohort` API. We still catch all our errors, too! The key to making this work is the existential type (`*`). Instead of doing any typechecking at all on the arguments themselves, we pass their types exactly as-is to the function body, which attempts to cram them into an `Experiment` type. If we tried to use anything else, it won't work!

This is because Flow typechecks each function in a vacuum given its arguments. If we typed the arguments as `string`s, for example, Flow would have no idea that the arguments are actually string literals that correspond to keys in the `Experiment` type, and would complain that not all strings are fit to be the keys and values of an `Experiment`!

The existential type tells Flow that it can't typecheck this function in a vacuum; it needs to look at _exactly_ what gets passed into the function upon each invocation. In doing so, it preserves the fact that the string is a particular string literal, rather than saying "yep, this is a `string`!" and throwing out that valuable information. This probably has a knock-on effect on the amount of time it takes Flow to check your project, but at the scale we're using it, it hasn't been an issue at all. It also means that it won't work if you're doing anything that prevents Flow from statically analyzing the arguments to the `experimentInCohort` function -- maybe you're templating your experiment names at runtime to pass into the function, or reading them from some other non-literal source.

Another small, but nonetheless unfortunate side-effect is that since we're only assessing the correctness of the function arguments within the function itself, rather than at the call site, Flow's error messages throw an error pointing to `experimentInCohort` if an incorrect set of arguments is provided. This results in some error messages that are a little more confusing than the first approach, but they're still helpful enough that you'll be able to find and fix your typo without too much difficulty. Finally, engineers have to add their new experiment type to both the `Experiment` union type and the `Buckets` intersection type. But again, this is something that can be done quickly and caught easily in code review.

If there's one ask I have of the Flow team, it's that this manipulation of large numbers of types be made easier. I'd love to be able to make a set of types and easily union, intersection, and pick from them without having to spend time finding these hacks.

That's all I've got. I wanted to use a union type in Flow to typecheck function arguments based on each others' values, and dammit, I pulled it off. Hope it helped!