// Setup your quiz text and questions here

// NOTE: pay attention to commas, IE struggles with those bad boys

var quizJSON = {
    "info": {
        "name":    "Dumb or Smart?",
        "main":    "<p>If you're at ONA, you probably have a smartphone (and then some). But the majority of people around the world -- and certain demographics -- in the U.S. only have dumbphones, old-school cell phones without internet or data plans. Take our quiz, based on an ONA talk by Susan McGregor and a recent Pew Research Center study, to find out if you should be thinking more about designing for phones that only have voice and text capabilities.</p>",
        "results": "<p>“Mobile” has been a buzzword in the journalism industry for a few years now, but it’s easy to forget that millions of people still can’t afford to get the latest smartphone, tablet, or wearable device. While mobile phones are becoming increasingly popular, the hottest technology isn’t evenly distributed.<br><br>So what are some ways to reach these audiences? SMS services like <a href=\"http://www.mobilecommons.com\">Mobile commons</a>, <a href=\"https://groupme.com\">GroupMe</a>, and <a href=\"http://www.tatango.com/\">Tatango</a>, can poll audiences and allow for group messaging. Radio station <a href=\"http://www.pbs.org/idealab/2011/01/how-wnyc-used-texts-from-citizens-to-map-snowstorm026/\">WYNC</a> used SMS-based surveys to crowd-source text and audio reports from the community during a snowstorm. In the southwest, SMS alerts can reach migrant labor communities that have limited access to the Internet.<br><br>And remember, just because sending an SMS is cheap, doesn’t mean an SMS service can’t be profitable. M-Pesa, a money-transferring service in Kenya, has 17 million registered users – you do the math.</p>",
        "level1":  "You should design for a dumbphone-heavy audience, which means think about using text/SMS services in creative ways.",
        "level2":  "You may like to consider designing for dumbphones. Read on to learn more.",
        "level3":  "Seems like you're kind of in the middle. You can design for smartphones, but if broad reach is important to you, don't forget about dumbphone users! Read on to learn more.",
        "level4":  "Your audience is probably smartphone-heavy. But if you do decide to design for dumbphones to broaden your reach, read on for some tools you can use." // no comma here
    },
    "questions": [
        { // Question 1 - Multiple Choice, Single True Answer
            "q": "Where is your target audience?",
            "a": [
                {"option": "U.S.",      "correct": false},
                {"option": "Somewhere else",     "correct": true},
             
            ],
            "correct": "<p><span>DUMB</span> Consider designing for a dumbphone. There are 3.5 billion mobile connections in Africa, the Middle East, Latin America and the Asia-Pacific regions -- the majority of these connections are probably in dumbphones. </p>",
            "incorrect": "<p><span>SMART</span> According to a recent Pew Research study, 57 percent of all Americans now have a smartphone. But a significant chunk of Americans still rely on dumbphones. Go on to the next question to see what you should do. </p>" // no comma here
        },
      /*  { // Question 2 - Multiple Choice, Multiple True Answers, Select Any
            "q": "Which of the following best represents your preferred breakfast?",
            "a": [
                {"option": "Bacon and eggs",               "correct": false},
                {"option": "Fruit, oatmeal, and yogurt",   "correct": true},
                {"option": "Leftover pizza",               "correct": false},
                {"option": "Eggs, fruit, toast, and milk", "correct": true} // no comma here
            ],
            "select_any": true,
            "correct": "<p><span>Nice!</span> Your cholestoral level is probably doing alright.</p>",
            "incorrect": "<p><span>Hmmm.</span> You might want to reconsider your options.</p>" // no comma here
        },
        { // Question 3 - Multiple Choice, Multiple True Answers, Select All
            "q": "Where are you right now? Select ALL that apply.",
            "a": [
                {"option": "Planet Earth",           "correct": true},
                {"option": "Pluto",                  "correct": false},
                {"option": "At a computing device",  "correct": true},
                {"option": "The Milky Way",          "correct": true} // no comma here
            ],
            "correct": "<p><span>Brilliant!</span> You're seriously a genius, (wo)man.</p>",
            "incorrect": "<p><span>Not Quite.</span> You're actually on Planet Earth, in The Milky Way, At a computer. But nice try.</p>" // no comma here
        },*/
        { // Question 4
            "q": "How old is your target audience?",
            "a": [
                {"option": "Over 65",    "correct": true},
                {"option": "Under 65",     "correct": false},
          
            ],
            "correct": "<p><span>DUMB</span> ou should probably assume your target audience has a dumbphone. According to the Pew Research Center, only 18% of American seniors have smartphones.</p>",
            "incorrect": "<p><span>SMART</span> The majority of people in the U.S. under 65 have smartphones. Younger audiences are more likely they are to have a smartphone-- a whopping 81 percent of Americans between 25 and 34 have smartphones</p>" // no comma here
        },
        { // Question 5
            "q": "Is your audience rural or urban?",
            "a": [
                {"option": "Rural",    "correct": true},
                {"option": "Urban",     "correct": false} // no comma here
            ],
            "correct": "<p><span>SMART</span> Rural audiences are more likely to have a dumbphone.</p>",
            "incorrect": "<p><span>DUMB</span> Urban audiences are more likely to have a smartphone.</p>" // no comma here
        }, // no comma here

		  { // Question 4
	            "q": "Is your audience primarily making $30,000 a year or less?",
	            "a": [
	                {"option": "Yes",    "correct": true},
	                {"option": "No",     "correct": false},

	            ],
	            "correct": "<p><span>DUMB</span> Only 43 percent of Americans making less than $30,000 own a smartphone.</p>",
	            "incorrect": "<p><span>SMART</span> The majority of those making above $30K own a smartphone. </p>" // no comma here
	        }


    ]
};
