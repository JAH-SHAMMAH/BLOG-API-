from fastapi import APIRouter, Depends, HTTPException, status


SHAMz = APIRouter(tags=["your eyes only ;)"])


@SHAMz.get("/home", description="reminder: JESUS is great!")
def home():
    return {"WELCOME TO THE SHAMMAH & JAH-MAN - what's it that you seek? we get am"}


@SHAMz.get("/about", description="KEEP IT POSITIVE!")
def about_us():
    return {"we share mysteries and other educating stuff plus music news but beware: for in much wisdom is much grief and he who chooses to increase in knowledge increases in sorrow"}


@SHAMz.get("/contacts", description="HELLO, 911? SOMEONE'S TRYING TO CONTACT ME :/")
def contact_us():
    return {"send a mail to: shamzyjayy@gmail.com",
            "find us on instagram @shamz_gram",
            "reach us on snapchat@shamz3760"
            }
