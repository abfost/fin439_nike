What is look-ahead bias?

Look-ahead bias happens when a backtest uses information that would not have been available at the time of the decision.


How do event time, publication time, and revisions matter?

Event time is the month the data measures. Publication time is when the number becomes available. A revision is a later update to an earlier number. For a decision on a particular date, we can use only publications and revisions available by that date.


Why does AAA’s +5.83% look better than what we could have known?

It uses AAA’s March value, which wasn’t published until April 10. On March 31, the latest available month was February, with a signal of +1.98%.


Which rule removed the row that mattered most?

I would choose rule 3, which removed rows published after the decision date. It removed AAA’s March value, preventing us from using information that wasn’t available yet. Rule 4 also mattered because it replaced AAA’s original February value with the revision.


What might a backtest using the naive column claim?

It might claim a strategy performed better than it actually could have, because it uses data that had not yet been published. The effect isn’t always an improvement: BBB’s naive signal is more negative than its as-of signal.


Partner: What is the difference between the month a number measures and the date it was published? 

The month measured is the month the data describes and the publication date is the day the data became available. For example, AAA’s row 4 measures February 2026, but it wasn’t published until March 25. That means someone making a decision on March 31 could use it, but someone making a decision on March 20 could not.