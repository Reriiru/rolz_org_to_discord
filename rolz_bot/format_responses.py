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

There is a tarot feature, that will give you a randomized tarot card:
!tarot
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

vibe_string = '''
Ｖｉｂｅ　ａｗａｙ，　ｂｏｙｏｓ！
https://www.youtube.com/watch?v=QXuIwJfwVf8
'''

shitpost_string = '''
*flings a shitty picture*
{}
'''

pesel_string = '''
**Have a pesel!**
{}
'''

response_error_string = '''
Error! Rolz wont bloody respond!
'''

hydra_string = '''
`Hail Hydra!`
{}
'''

neko_string = '''
*shamelesly ripping off features*
{}
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

sum_string =  '''
Sum rolls are now in for: **{}**
'''

sum_results_string = '''
Sum result is: `{}`
'''

sum_details_string = '''
Here are some details:
'''

nwod_response = '''
Nwod roll results are in for **{}**:
Result: `{}`
Details: `{}`
'''

tarot_response = '''
Tarot is in for **{}**:
{}
'''