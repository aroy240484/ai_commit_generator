# ai_commit_generator
Generative AI powered commit message generator

Uses Anthropic's Claude 3 Sonnet to generate commit message for the diff provided

Usage:

1. Run setup (make sure you have execute permission `sudo chmod +x setup.sh`)
```
./setup.sh
```

2. Make changes to your local repo and stage the changes
```
git add .
```

3. Run the commit CLI
```
commit
```

This should generate a descriptive commit message for the diff provided.

Enjoy!
