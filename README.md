# anydo2trello
This script imports your tasks from [any.do](https://www.any.do) and converts them to boards and cards in [trello](https://www.trello.com). I particularly did this after the anydo 3.0 update which I didn't like so decided to shift all my notes to my trello account which I used for work purposes.

This script does the following to convert any.do data to trello

|**AnyDo**|**Trello**|
|---|---|
|Categories|Boards|
|Tasks|Cards
|Notes|Description|
|Sub tasks|Checklist|

By default all the **unchecked** tasks are added to **To Do** list of a board and **checked** tasks are added to **Done** list of a board. Feel free to change them as you wish to from the script.

**Disclaimer:**
This script does not store any of your data. The current implementation for anydo login is very naive and directly asks for username and password but are not stored anywhere. I'll try to include OAuth later.
