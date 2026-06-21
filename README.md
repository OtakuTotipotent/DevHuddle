# Notes About DevHuddle

This document contains various notes and ~~observations~~/guidelines regarding "DevHuddle" platform, including future improvements, new features, fixes, and general concepts.

## Setup & Installations

- Install **Python** if not already
- Open project in IDE/Terminal ~~(like VSCode/Powershell)~~
- Create Python Virtual Environment, and activate it:

```cmd
python -m venv .venv
.venv\Scripts\Activate
```

- Install _Python Dependencies_:

```cmd
pip install -r requirements.txt
```

- Install _TailwindCSS_ & other _JS Dependencies_ (use separate/independent terminal window):

```cmd
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
