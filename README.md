1. Team Name: TAJ
2. Team Members:
	- Tim Contois tcontois@umass.edu UMass Amherst CS Masters
	- Alex Lassalle alassall@umass.edu UMass Amherst CS Masters
	- Andrew Gramigna agramign@umass.edu UMass Amherst CS Masters
	- Josh Pikovsky jpikovsk@umass.edu UMass Amherst CS Masters
3. Advisor: N/A
4. Solution:
Our idea was to put the n-grams into "states". State 0 was the base state and for every length one n-gram (and every first word of longer n-grams) there is a transition for state 0 to that state. For 2-grams, it reuses a 1-gram state if one existed. For example, n-grams "hello" and "hello there" would both use the same "hello" state. We used this strategy for all length n-grams. We also stored which states had output. In the "hello" and "hello there" example, the "hello" state would output "hello" and the "there" state linked from "hello" would output "hello there". In the example of "the dog and cat," only the "cat" state would have output.
To query a document, we only look at transitions from a specific set of states. We always looked from the base state, but additionally we would look from whatever state/(s) the previous word left us in.
To avoid sorting the n-grams in the correct order at the end, we used buckets. We made the number of buckets equal to the length of the longest n-gram. With this strategy we could safely empty one bucket in each iteration of the loop through the document. When we found a new n-gram we placed it in the correct bucket corresponding to it's start location. Within the same bucket (same starting index), no sorting was needed because shorter n-grams where placed in the bucket first.