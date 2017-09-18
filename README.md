# BlackJackBot

BlackJackBot was developed at [Aveiro University](https://www.ua.pt) in the course [47139-Introduction to Artificial Intelligence](http://www.ua.pt/ensino/uc/28http://www.ua.pt/ensino/uc/2494) for academic purposes and intents to demonstrate the steps needed to implement a blackjack agent with reinforcement learning.

## How the agent learn and play?

The agent learns from its mistakes *(Reinforcement Learning)*.
To take one decision, the agent has a disctionary with a key(state) containing all the information obtained in those plays:
key = (valueInHand, dealerValue, softAceInHand, dealerAceInHand, dealerAction, firstTurn)

To learn and produce valid information the agent needs to do 200 *(hits)* and *(stands*) to the same state, in order to initialize the odds relative to profit(hit, stand).

After the initial learning, the agent will decide his play by the 'decision' that is most likely to succeed with the update of the odds according to the final result of that game.

During a game, the shifts are stored in a buffer and according to the final result, the update is done by traversing the buffer and assigning wins to each state.

The hitProfit is calculated through the hitWin and hitLose of each saved state, the same applies to the stand and doubleDown.

To surrender, a checkSurrender function was used that receives the highest profit (hit, stand or dd) and makes a calculation similar to surrender itself, that is, see if it is more advantageous to win half the bet (surrender) than to opt for another decision (hit, stand, dd)

At the end of 5000 games, the states/results in the dictionaries are updated to the file(cheats).

The agent experienced a total of 15 million games in his learning and has a victory rate of approximately 52%.

## Remark

All the game was developed and provided by the course teacher. Only the agent was developed by me, present in the file *(student.py)*.

## Licence

MIT