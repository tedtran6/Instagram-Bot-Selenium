# Instagram-Bot-Selenium

This is a bot created for Instagram with the purpose of following users and liking photos.

I originally wanted to create this bot as a means to gain followers, and since the creation of the bot, I've been able to gain a significant amount of followers on my account. The niche that my instagram account was in is the "meme" posting niche, where I would repost funny and relatable content for users of instagram to consume. 

I was able to create this bot using Selenium and using the *inspect* button on Google Chrome

<img src = "images/image1.png" width = "700">

The strategy that I deploy here is unique from most bots that I've seen around the internet, and I'll go more in depth about that later down in this description.

I primarily wanted to start very low level with my development of this software. In particular, I got the functionality of following and liking photos down first. After this, I created the functionality of following users who comment on a particular post. Then I created the function of following users who comment on a particular *set* of posts that a popular account has in their most recent feed. 

The particular strategy I was aiming for was in order to get the maximum amount of followers from using this bot was:
1. Compile a list of popular meme accounts and funny accounts, and cycle through them
2. Compile a list of the most recent posts a popular meme account has posted on their account
3. Compile a list of the users who have commented on these posts who **tag their friends**
4. Go to the users profile who tagged their friend, and if their account is:
    1. Private: Request to follow them, and move on.
    2. Public: Follow the user, and then like their most recent photo.
    
From this strategy we should be able follow quite a bit of people. 

I also included a lot of other ways to interact with Instagram and Instagram audiences, but this really seemed like the most effective way to gain followers. 

## Notes

The project was compiled in python 3.7
