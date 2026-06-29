# Notes About DevHuddle

This document contains various notes and ~~observations~~/guidelines regarding "DevHuddle" platform, including future improvements, new features, fixes, and general concepts.

## Live ?

- [Click here to jump to the Previews section.](#preview)
- Project is under maintenance.
- Discuss in private? DM [@LinkedIn](https://www.linkedin.com/in/afnanmuhammad "linkedin/afnanmuhammad")

## Setup & Installations

- Install **Python** if not already
- Open project in IDE/Terminal ~~(like VSCode/Powershell)~~
- Create Python Virtual Environment, and activate it:

```python
python -m venv .venv
.venv\Scripts\Activate
```

- Install _Python Dependencies_:

```python
pip install -r requirements.txt
```

- Install _TailwindCSS_ & other _JS Dependencies_ (use separate/independent terminal window):

```js
npm install
```

- Run project (Python oriented terminal window),(Run following commands separately, one by one). The last command will give a link address to be used (copy/paste to any browser):

```cmd
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Run JS related libs as follows (Tailwind requires continuous background running):

```cmd
npx @tailwindcss/cli -i ./static/css/custom.css -o ./static/css/output.css --watch
```

## Dev: Extensions Used

- [djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
- [Python Extensions Pack](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
- [Django](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
- [Markdownlint](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)
- [TailwindCSS Intelligence](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-extension-pack)

## Major Fixes

- On same web browser, logging in/out should not interfere with each other for multiple tabs.
- Add favicon
- Add user guides for DevHuddle
- Apply SEO
- Add 'about', 'help & support', 'Jobs & Clients' page links into footer for large screens
- Delete profiles/user accounts only after 3 days, not immediately
- Add Recycle bin page for recovering data within 3 days
- Add Notifications tone/music
- The Subscription (DevHuddle Pro) needs to be ended after certain time period (monthly)
- Add dynamic data into profile stats

## Improvements \& Suggestions

- Relevant accounts suggestions based on user activity and interests (On Right Side).
- Relevant jobs, projects, gigs \& contests suggestions based on user activity and interests (On Left side).
- Relevant accounts and Relevant Jobs sections in the Business, Global, Advertisers sections on feed.
- Enhanced search functionality with filters for content type, date, and popularity.
- Add notifications
- Implement light theme.
- Add a dedicated page for jobs, projects, gigs \& contests.
- While posting selecting a category of post, that will display relevant posts to TARGET or ACTIVE audience as well as profile visitors. Also adding options like formatted/HTML like text uploading in post and prohibiting the video uploads.
- A Network page for showcasing all users with whom the user has collaborated

## Preview

![Homepage](./static/images/unauthorized.png/ "Unauthorized User Homepage view")
![Homepage](./static/images/homepage.png/ "Authorized User Homepage view")
![Homepage](./static/images/devs-directory.png/ "Developers Leaderboard view")
![Homepage](./static/images/messages.png/ "Inbox/Messenger view")
![Homepage](./static/images/notifications.png/ "Notifications view")
![Homepage](./static/images/profile.png/ "User Profile view")
![Homepage](./static/images/workspace.png/ "Clients view")
![Homepage](./static/images/dashboard.png/ "Dashboard view")
![Homepage](./static/images/subscriptions.png/ "Store/Subscriptions page view")
![Homepage](./static/images/mobile.png/ "Small Screen/Mobile Phone view")
