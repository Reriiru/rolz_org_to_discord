help_string = '''
This bot proxies your rolls to rolz.org.
Syntax info can be found here:
https://rolz.org/wiki/page?w=help&n=BasicCodes
```
To roll you use !roll. Example:
!roll 6d6
It can use multiple rolls with !sum and !repeat. Example:
!sum 5 1d6
!repeat 5 1d6
It can also use choose. Example:
!choose Love, Marry, Kill

I have added full support for the nwod dice. Specific format for
success based dice for cofd and nwod. Here is how you use it:
!nwod 10 -- this roll 10 nwod dice.
!nwod r10 -- this rolls 10 nwod rote dice.
!nwod 10e8 -- this rolls 10 nwod dice with every 8 exploding.

Those can be combined, for example:
!nwod r10e8 -- will roll 10 nwod rote dice that explode on 8.

Have a look at FFG Warhammer 40K rolls. They work like this:
!wh 45 -- where 45 is your modified Characteristic score.

There is a tarot feature, that will give you a randomized tarot card:
!tarot

There is a value feature, that will store user specified value.
Limited by 1000 symbols.
To create a value use !value create. Example:
!value add "Spaceship" "Its a space walrus!"
To show a value use !value show. Example:
!value show "Spaceship" -- this will print you the value of Spaceship as defined earlier.
To show a list of defined values use !value list. Example:
!value list -- this will print you a list of your values.
To delete a defined value use !value delete "NAME". Example:
!value delete "Spaceship"
```
'''

roll_string = '''
**{}** Roll Result: `{}`, Roll Details: `{}`
'''

invalid_roll_string = '''
Please, use **valid** rolz codes.
You can find info on roll formats here:
https://rolz.org/wiki/page?w=help&n=BasicCodes
'''

weird_characters_string = '''
Enough with the weird characters, you ponce!
'''

choose_string = '''
I choose **{}**!
'''

response_error_string = '''
Error! Rolz wont bloody respond!
'''

message_too_long_string = '''
Stop trying to put something this large up discord's arse.
'''

repeat_string = '''
Repeat rolls are now in for: **{}**
'''

repeat_results_string = '''
Results are: ** |'''

repeat_details_string = '''
Here are some details:
'''

sum_string = '''
Sum rolls are now in for: **{}**
'''

sum_results_string = '''
Sum result is: `{}`
'''

sum_details_string = '''
Here are some details:
'''

nwod_string = '''
Nwod roll results are in for **{}**:
Result: `{}`
Details: `{}`
'''

invalid_value_string = '''
Macro value is invalid! Perhaps it's too long.
'''

value_added_string = '''
Macro value **{}** was succesfully added for user **{}**.
'''

value_search_error_string = '''
Something went wrong during search!
'''

value_nothing_found_string = '''
No such value exists!
'''

value_search_string = '''
Value **{}** for **{}**:
'''

value_update_string = '''
Value **{}** for **{}** updated.
'''

value_list_string = '''
List of values for **{}**:
{}
'''

value_list_empty_string = '''
Empty list of values for **{}**.
'''

value_delete_none_string = '''
No value to delete!
'''

value_delete_fail_string = '''
Error occured during delete. Sorry!
'''

value_delete_string = '''
Value **{}** for **{}** deleted.
'''

wh_string_fail = '''
FFG Warhammer roll is in for **{}**.
Roll results: `{}` Degrees of failure: `{}`
'''

wh_string_success = '''
FFG Warhammer roll is in for **{}**.
Roll results: `{}` Degrees of success: `{}`
'''
