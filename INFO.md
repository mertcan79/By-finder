source .venv/bin/activate     

Celery: celery -A tasks worker --loglevel=info -c 5  
Redis: redis-server  


MongoDB U: mertcan-coskun
MongoDB PW: Zg8iO4z7X7Nt0LdJ

MongoDB group id = 6360482397a05a183d73f31b

mongo mongodb://127.0.0.1:27017 --username mertcan-coskun --password Zg8iO4z7X7Nt0LdJ

mongo mongodb://<hostname>:<port> --username <your-username> --password <your-password>


git remote set-url origin https://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@github.com/mertcan79/byfinder.git

git remote set-url origin git@github.com:mertcan79/byfinder.git

killall ssh-agent; eval `ssh-agent`

git remote set-url origin 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@github.com:mertcan79/byfinder.git 

df_history = pd.DataFrame({
    'SearchRooms': np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1], size=N),
    'SearchSqft': np.random.choice(['small', 'medium', 'large'], p=[0.2, 0.6, 0.2], size=N),
    'SearchQuality': np.random.choice(['low', 'medium', 'high'], p=[0.2, 0.6, 0.2], size=N),
    'SearchPrice': np.random.choice(['low', 'medium', 'high'], p=[0.1, 0.2, 0.7], size=N),
    'IndustryRooms': np.random.choice([1, 2, 3], size=N),
    'IndustrySqft': np.random.choice(['small', 'medium', 'large'], size=N),
    'IndustryQuality': np.random.choice(['low', 'medium', 'high'], size=N),
    'IndustryPrice': np.random.choice(['low', 'medium', 'high'], size=N),
    'Rooms': np.random.choice([1, 2, 3], size=N),
    'Sqft': np.random.choice(['small', 'medium', 'large'], size=N),
    'Quality': np.random.choice(['low', 'medium', 'high'], size=N),
    'Price': np.random.choice(['low', 'medium', 'high'], size=N),
    'UserPref': np.random.choice(['like', 'neutral', 'dislike'], size=N)
})