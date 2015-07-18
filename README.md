# Tournament
A basic swiss ranking tournament database that assumes there are even number of competitors

## Table of contents

- [What's included](#What's included)
- [Creators](#creators)
- [Copyright and license](#copyright-and-license)

### What's included
This repository contains the python and sql files for the tournament results

```
tournament/
├── tournament.py
├── tournament_test.py
└── tournament.sql
```

## Software Requirements

Python 2.7.10

PostgreSQL 9.5


## Setup Instructions

### Database creation

1. Navigate to the tournament directory in command line or terminal
2. Start PostgreSQL using command 'psql'
3. Create the database using command '\i tournament.sql'

### Tournament & Testing

1. Navigate to the tournament directory in command line or terminal
2. Run the tournament python script with command 'python tournament.py'
3. To see the unit testing run command 'python tournament_test.py'


## Creators

**Dillon Keith Diep**


## Copyright and license

The code released was created for educational purposes, copyright and license subject to Udacity's provided source code - no other enforcements otherwise.
