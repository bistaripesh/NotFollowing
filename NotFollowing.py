from argparse import ArgumentParser
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

try:
    from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
    raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
    print("Using cookies from {}.".format(cookiefile))
    conn = connect(cookiefile)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-c", "--cookiefile")
    p.add_argument("-f", "--sessionfile")
    args = p.parse_args()
    try:
        import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
    except (ConnectionException, OperationalError) as e:
        raise SystemExit("Cookie import failed: {}".format(e))
import instaloader

# Get instance
L = instaloader.Instaloader()


USER = input("Enter your username: ")
PASSWORD =input("Enter your password: ")
#profile = instaloader.Profile.from_username(L.context, "prada")
L.login(USER, PASSWORD)    
profile = instaloader.Profile.from_username(L.context, USER)
followers = list()
followees = list()
for x in profile.get_followers():
    #def get_followers():
    followers.append(x.username)
        #return x.username
for y in profile.get_followees():
    followees.append(y.username)

notfollowing = list(set(followees) - set(followers))
for x in range(len(notfollowing)):
    print(str(notfollowing[x])+" is not following you")
print("---------------------------------------------")
print(str(len(notfollowing))+" people are not following you")
'''
q = list()
for f in range(len(followees)):
    for n in range(len(followers)):
        if(followees[f]==followers[n]):
            q.append(followers[n])
          #  print(str(followers[n])+" follows you")
notfollowing = list()
for a in range(len(followees)):

    for b in range(len(q)):
        if(followees[a]==q[b]):
            print() 
        else:
            notfollowing.append(followees[a])
            #print(str(followees[a])+"doesn't follows you")
        
notfollowing = list(dict.fromkeys(notfollowing))
for j in range(len(notfollowing)):
    print(notfollowing[j])
'''