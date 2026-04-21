# Ant Sandbox North Star v1

## Purpose

This document states the north star for the new ant-sandbox branch.

It exists because the earlier ecology-graph world can remain useful as a
reference, but it is not the world type we actually want to watch.

## The Project In One Sentence

Build a watchable artificial ant colony sandbox where many small agents live in
local space, search for food, return to a nest, leave traces, recover from
disturbance, and gradually form colony-level structure.

## What We Actually Want To See

The desired world should feel like:

- a place rather than a chart
- a colony rather than a bag of particles
- local movement rather than graph jumps
- visible work rather than only hidden metrics

More concretely, we want:

- ants moving in local space
- a nest as a real location
- food patches as real targets
- carrying, returning, and unloading behavior
- trails or local trace fields
- colony recovery after disruption

## What This World Is Not

This branch is not trying to be:

- a habitat-graph metapopulation model
- a dashboard-first ecology panel
- an inheritance-research platform before colony behavior exists

Those may remain useful background lines.
They are not the main sandbox target.

## Promotion Rule

Do not prioritize higher-order mechanism work until the sandbox has visibly
passed:

- spatial realism
- foraging loop
- pheromone effectiveness

The sandbox must first feel alive at the local level.

## Immediate Design Consequence

The new main-line substrate must start from:

- local 2D or fine local grid space
- nest
- food
- ants as many visible agents
- simple local sensing
- simple local movement
- a trace field placeholder

That is the shortest path to the world type we actually want.
