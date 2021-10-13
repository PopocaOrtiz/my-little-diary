# my-little-diary
Web App for writing a personal diary using social media features

- entries are saved as short messages insted of large posts
- tags can be created using # 
- people can be identified using @ 

# current features 

# todo list v1
- [x] post an entry 
- [x] list (last) entries
- [x] search entries
- [x] paginate entries
- [x] when posting an entry also save tags
- [x] filter by tag using the search box (#)
- [ ] highligh tags when showing entries
- [ ] click in (highlighted) tags to filter entries
- [ ] when posting an entry also save people
- [ ] filter by people using the search box (@) 
- [ ] highligh people when showing entries
- [ ] click in (highlighted) people to filter entries

# todo list v2
- [ ] attach photos to entries 
- [ ] people's profile
 - [ ] show a short description
 - [ ] show last messages(and paginate)
 - [ ] show last tags(and how many time they are used)
 - [ ] show relations with other people

# requirements
- python
- flask
- sqllite
- python-dotenv

# run
```
export FLASK_APP=server.py
```