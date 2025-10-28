def get_all_users():
    users = [
    {
    "id": 1,
    "name": "Dimond",
    "description": "A well known dev.",
    "website": "http://smartlearning.liveblog365.com/dimond",
    "email": "diamondkudzai70@gmail.com",
    "phone": "012 345 6789",
    "image" : "image1.png",
    "skills": ["Christ Follower","Developer","SmartLearning"],
    "clustersCount" : 7,
    "notificationsCount" : 4,
    "location": "Caribian",
    "messages":["Doing great","We expect more","we will get there"]
    },
    {
    "id": 2,
    "name": "JohnDoe",
    "description": "A musician and Description for second user.",
    "website": "https://github.com/dimondkudzai",
    "email": "contact@secoggnduser.co.za",
    "phone": "+2712 345 6790",
    "image" : "image2.png",
    "skills": ["Design","Art","Creativity"],
    "clustersCount" : 0,
    "location": "Jamaica",
    "notificationsCount" : 10,
    
    },
    {
    "id": 3,
    "name": "ChrisVoiloe",
    "description": "Here is Description for Chris user.",
    "website": "http://smartlearning.liveblog365.com/dimond/index.html",
    "email": "contact@seconduser.co.za",
    "phone": "+2712 345 6790",
    "image" : "image3.png",
    "skills": ["Public Speaking","Motivator","Counceling"],
    "clustersCount" : 9,
    "notificationsCount" : 8
    
    },
    {
    "id": 4,
    "name": "VictorPose",
    "description": "Description for Victor Pose.",
    "website": "www.sPruser.co.za",
    "email": "contact@seconfghduser.co.za",
    "phone": "012 345 6790",
    "image" : "image4.png",
    "skills": ["Real estate","Construction","Legal"],
    "clustersCount" : 8,
    "notificationsCount" : 4,
    },
    {
    "id": 5,
    "name": "KnosiDube",
    "description": "A lawyer in SA.",
    "website": "www.sgueconduser.co.za",
    "email": "contact@setcondghuser.co.za",
    "phone": "+26312 345 6790",
    "image" : "image5.png",
    "skills": ["Marketing","Business","Analysis"],
    "clustersCount" : 1,
    "notificationsCount" : 3,
    
    }
    ]
    return users
    
def get_all_clusters():
	clusters = [
	{
	"id": 1,
	"name": "Creative Writers",
	"target": "Let's build Apps",
	"author": "ChrisVoiloe",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["VictorPose", "KnosiDube", "Dimond"],
	"conversations": [
	{
	"chatId": 100,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe",
	"body": "Lets start working guys",
	"created": "2025-10-22T10:05:00Z",
	"comments": [
	{"user": "VictorPose", "text": "Excited to write!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "KnosiDube", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	},{
	"chatId": 101,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe",
	"body": "Lets start working guys",
	"created": "2025-10-22T10:05:00Z",
	"comments": [
	{"user": "VictorPose", "text": "Excited to write!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "KnosiDube", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	}
	]
	},
	{
	"id": 2,
	"name": "Native buider",
	"target": "Launching",
	"conversations": [
	{
	"chatId": 106,
	"title": "Kickoff Meeting",
	"body": "Let's brainstorm the app structure.",
	"author": "ChrisVoiloe",
	"comments": [
	{
	"user": "VictorPose",
	"text": "Excited to write!",
	"timestamp": "2025-10-22T10:00:00Z"
	},
	{
	"user": "KnosiDube",
	"text": "Let's go!",
	"timestamp": "2025-10-22T10:05:00Z"
	}
	]
	}
	]
	},
	{
	"id": 3,
	"name": "Legal Minds",
	"author": "LegalBoss",
	"members": ["LegalBoss", "VictorPose", "Admin1"],
	"location": "International",
	"conversations": [
	{
	"chatId": 103,
	"title": "Case Reviews",
	"author": "LegalBoss",
	"comments": [
	{"user": "Admin1", "text": "We should meet next week.", "timestamp": "2025-10-20T09:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-15T14:45:00Z"
	},
	{
	"id": 4,
	"name": "Design Lab",
	"author": "AnnaSmith",
	"location": "Harare",
	"members": ["AnnaSmith", "SketchMaster", "PixelHero"],
	"conversations": [
	{
	"chatId": 104,
	"title": "Color Theory",
	"author": "AnnaSmith",
	"comments": [
	{"user": "SketchMaster", "text": "Love this topic!", "timestamp": "2025-10-18T11:30:00Z"}
	]
	}
	],
	"created_at": "2025-10-16T07:00:00Z"
	},
	{
	"id": 5,
	"name": "Motivators",
	"author": "ChrisVoiloe",
	"location": "International",
	"members": ["ChrisVoiloe", "InspireZim", "ShineOn"],
	"conversations": [
	{
	"chatId": 105,
	"title": "Daily Quotes",
	"author": "InspireZim",
	"comments": [
	{"user": "ShineOn", "text": "Keep pushing!", "timestamp": "2025-10-21T15:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-17T08:15:00Z"
	},
	{
	"id": 6,
	"name": "Creative Writers",
	"author": "ChrisVoiloe",
	"members": ["ChrisVoiloe", "VictorPose", "AnnaSmith"],
	"conversations": [
	{
	"chatId": 101,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe",
	"comments": [
	{"user": "VictorPose", "text": "Excited to write!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "AnnaSmith", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	}
	],
	"created_at": "2025-10-20T08:00:00Z"
	},
	{
	"id": 7,
	"name": "Tech Founders",
	"author": "VictorPose",
	"members": ["VictorPose", "DevKing", "CodeQueen"],
	"conversations": [
	{
	"chatId": 102,
	"title": "Startup Ideas",
	"author": "VictorPose",
	"comments": [
	{"user": "CodeQueen", "text": "AI is the future.", "timestamp": "2025-10-21T12:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-19T13:20:00Z"
	},
	{
	"id": 8,
	"name": "Legal Minds",
	"author": "LegalBoss",
	"members": ["LegalBoss", "VictorPose", "Admin1"],
	"conversations": [
	{
	"chatId": 103,
	"title": "Case Reviews",
	"author": "LegalBoss",
	"comments": [
	{"user": "Admin1", "text": "We should meet next week.", "timestamp": "2025-10-20T09:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-15T14:45:00Z"
	},
	{
	"id": 9,
	"name": "Design Lab",
	"author": "AnnaSmith",
	"members": ["AnnaSmith", "SketchMaster", "PixelHero"],
	"conversations": [
	{
	"chatId": 104,
	"title": "Color Theory",
	"author": "AnnaSmith",
	"comments": [
	{"user": "SketchMaster", "text": "Love this topic!", "timestamp": "2025-10-18T11:30:00Z"}
	]
	}
	],
	"created_at": "2025-10-16T07:00:00Z"
	},
	{
	"id": 10,
	"name": "Motivators",
	"author": "ChrisVoiloe",
	"members": ["ChrisVoiloe", "InspireZim", "ShineOn"],
	"conversations": [
	{
	"chatId": 105,
	"title": "Daily Quotes",
	"author": "InspireZim",
	"comments": [
	{"user": "ShineOn", "text": "Keep pushing!", "timestamp": "2025-10-21T15:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-17T08:15:00Z"
	},
	{
	"id": 11,
	"name": "Creative Writers",
	"author": "ChrisVoiloe",
	"members": ["ChrisVoiloe", "VictorPose", "AnnaSmith"],
	"conversations": [
	{
	"chatId": 101,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe",
	"comments": [
	{"user": "VictorPose", "text": "Excited to write!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "AnnaSmith", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	}
	],
	"created_at": "2025-10-20T08:00:00Z"
	},
	{
	"id": 12,
	"name": "Tech Founders",
	"author": "VictorPose",
	"members": ["VictorPose", "DevKing", "CodeQueen"],
	"conversations": [
	{
	"chatId": 102,
	"title": "Startup Ideas",
	"author": "VictorPose",
	"comments": [
	{"user": "CodeQueen", "text": "AI is the future.", "timestamp": "2025-10-21T12:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-19T13:20:00Z"
	},
	{
	"id": 13,
	"name": "Legal Minds",
	"author": "LegalBoss",
	"members": ["LegalBoss", "VictorPose", "Admin1"],
	"conversations": [
	{
	"chatId": 103,
	"title": "Case Reviews",
	"author": "LegalBoss",
	"comments": [
	{"user": "Admin1", "text": "We should meet next week.", "timestamp": "2025-10-20T09:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-15T14:45:00Z"
	},
	{
	"id": 14,
	"name": "Design Lab",
	"author": "AnnaSmith",
	"members": ["AnnaSmith", "SketchMaster", "PixelHero"],
	"conversations": [
	{
	"chatId": 104,
	"title": "Color Theory",
	"author": "AnnaSmith",
	"comments": [
	{"user": "SketchMaster", "text": "Love this topic!", "timestamp": "2025-10-18T11:30:00Z"}
	]
	}
	],
	"created_at": "2025-10-16T07:00:00Z"
	},
	{
	"id": 15,
	"name": "Motivators",
	"author": "ChrisVoiloe",
	"members": ["ChrisVoiloe", "InspireZim", "ShineOn"],
	"conversations": [
	{
	"chatId": 105,
	"title": "Daily Quotes",
	"author": "InspireZim",
	"comments": [
	{"user": "ShineOn", "text": "Keep pushing!", "timestamp": "2025-10-21T15:00:00Z"}
	]
	}
	],
	"created_at": "2025-10-17T08:15:00Z"
	}
	
	]
	return clusters