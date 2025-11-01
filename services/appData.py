def get_suggestions():
    skills = ["Frontend", "Backend", "DevOps", "Marketing", "Finance"]
    return skills
def get_all_users():
    users = [
    {
    "id": 1,
    "name": "Dimond",
    "full_name": "Dimond Madechawo",
    "description": "A well known software dev.",
    "website": "http://smartlearning.liveblog365.com",
    "email": "diamondkudzai70@gmail.com",
    "phone": "012 345 6789",
    "password": "chimboza@1",
    "image" : "image1.png",
    "skills": ["Health","Finance","Farmer","Software developer"],
    "clustersCount" : 7,
    "created_clusters": [1,2,7,12,4,1],
    "clusters_requests": [1,2,7,6,9,4,5],
    "notificationsCount" : 4,
    "location": "Zimbabwe",
    "messages":[{
    "id": 1,
    "body": "Your request to join 'Tech Builders' was accepted: 'Glad to have you!'",
    "read": False,
    "timestamp": "2025 09 12 566 UTC",
    }]
    },
    {
    "id": 2,
    "name": "JohnDoe",
    "full_name": "Jon Deen Doe",
    "description": "A musician and Description for second user.",
    "website": "https://github.com/dimondkudzai",
    "email": "contact@secoggnduser.co.za",
    "phone": "+2712 345 6790",
    "password": "chimboza@1",
    "image" : "image2.png",
    "skills": ["Designer","Creativity"],
   "created_clusters": [13,6,7,12,14,1],
   "clusters_requests": [10,6,7,6,9,4,5],
    "notificationsCount" : 10,
    "clusters": [1,2,3,12,8,9],
    "location": "Zimbabwe",
	"messages": [
	    {
	        "id": 1,
	        "body": "Your request to join 'Tech Builders' was accepted.",
	        "read": False,
	        "timestamp": "2025-09-12 05:00 UTC",
	        "url": "/clusters/chat/5"
	    },
	    {
	        "id": 2,
	        "body": "You have a new follower: @ChrisDev",
	        "read": False,
	        "timestamp": "2025-09-13 09:30 UTC",
	        "url": "/users/Dimond"
	    }
	]
    
    },
    {
    "id": 3,
    "name": "ChrisVoiloe2",
    "full_name": "Chris Voiloe",
    "description": "Here is Description for Chris user.",
    "website": "http://smartlearning.liveblog365.com/dimond/index.html",
    "email": "contact@seconduser.co.za",
    "phone": "+2712 345 6790",
    "password": "chimboza@1",
    "image" : "image3.png",
    "skills": ["Public Speaking","Motivator","Counceling"],
    "clustersCount" : 9,
    "notificationsCount" : 8,
    "created_clusters": [1,6,7,12,14,15],
    "clusters_requests": [10,6,7,2,4,5],
    "location": "Jamaica",
    "messages":["@said something","We expect more","we will get there"]
    
    },
    {
    "id": 4,
    "name": "VictorPoseZw",
    "full_name": "Victor Pose",
    "description": "Description for Victor Pose.",
    "website": "www.sPruser.co.za",
    "email": "contact@seconfghduser.co.za",
    "phone": "012 345 6790",
    "password": "chimboza@1",
    "image" : "image4.png",
    "skills": ["Real estate","Construction","Legal"],
    "clustersCount": 0,
    "created_clusters": [10,6,7,1,14,5],
    "clusters_requests": [1,6,7,12,4,5],
    "notificationsCount" : 4,
    "location": "USA",
    "messages":["@Dimond said something","We expect more","we will get there"]
    
    },
    {
    "id": 5,
    "name": "KnosiDubeSA",
    "full_name": "Knosilazi Dube",
    "description": "A lawyer in SA.",
    "website": "www.sgueconduser.co.za",
    "email": "contact@setcondghuser.co.za",
    "phone": "+26312 345 6790",
    "password": "chimboza@1",
    "image" : "image5.png",
    "skills": ["Marketing","Business","Analysis"],
    "clustersCount" : 1,
    "created_clusters": [1,6,7,12,14,15],
    "clusters_requests": [10,6,7,2,4,5],
    "notificationsCount" : 3,
    "location": "Toronto",
    "messages":["@said something","We expect more","we will get there"]
    
    }
    ]
    return users
    
def get_all_clusters():
	clusters = [
	{
	"id": 1,
	"name": "Brain Flow AI",
	"target": "Building AI that solves health issues",
	"author": "Dimond",
	"created": "2025-10-22T10:05:00Z",
	"location": "International",
	"description": "Brain Flow AI is a project that aims to develop an AI tool that reads brain flow. This brain flow will be recorded, analyzed and used for medical treatment https://github.com/BrainFlowAi/BrainFlowAi.",
	"tags": ["ML", "AI", "Neurology","health"],
	"members": ["Dimond"],
	"conversations": [
	{
	"chatId": 1,
	"title": "Looking for early contributors",
	"author": "Dimond",
	"body": "Lets start working guys",
	"created": "2025-10-22T10:05:00Z",
	"comments": [
	{"user": "VictorPoseZw", "text": "Excited to contribute!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "KnosiDubeSA", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	},{
	"chatId": 2,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe2",
	"body": "Lets start working guys",
	"created": "2025-10-22T10:05:00Z",
	"comments": [
	{"user": "VictorPoseZw", "text": "Excited to start", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "KnosiDubeSA", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	}
	],
	"requests": [
	{
	"chatId": 1,
	"title": "known devloper",
	"body": "Let me join i bring tidings.",
	"author": "Dimond",
	"comments": [
	{
	"user": "VictorPoseZw",
	"text": "Yes sure",
	"timestamp": "2025-10-22T10:00:00Z"
	},
	{
	"user": "KnosiDubeSA",
	"text": "Let's go!",
	"timestamp": "2025-10-22T10:05:00Z"
	}
	]
	}
	]
	},
	{
	"id": 2,
	"name": "Fish Famers",
	"target": "Produce Breams for sale",
	"author": "Dimond",
	"created": "2025-10-22T10:05:00Z",
	"location": "Zimbabwe",
	"members": ["Dimond"],
	"description": "Fish production is cheap and there is market in Zimbabwe. With land and small capital much returns",
	"tags": ["Farmer", "Marketing", "Finance"],
	"conversations": [
	{
	"chatId": 1,
	"title": "Starting",
	"body": "Let's find land with dam or pond.",
	"author": "Dimond",
	"comments": [
	{
	"user": "VictorPoseZw",
	"text": "Yes sure",
	"timestamp": "2025-10-22T10:00:00Z"
	},
	{
	"user": "KnosiDubeSA",
	"text": "Let's go!",
	"timestamp": "2025-10-22T10:05:00Z"
	}
	]
	}
	],
	"requests": [
	{
	"chatId": 1,
	"title": "known devloper",
	"body": "Let me join i bring tidings.",
	"author": "Dimond",
	"comments": [
	{
	"user": "VictorPoseZw",
	"text": "Yes sure",
	"timestamp": "2025-10-22T10:00:00Z"
	},
	{
	"user": "KnosiDubeSA",
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"description": "Buiding Everything",
	"tags": ["smartlearning", "developer", "Designer"],
	"members": ["LegalBoss", "VictorPoseZw", "Admin1"],
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
	"location": "Panama",
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Co-founders", "DevOps"],
	"target": "Let's Design Apps",
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"location": "International",
	"target": "Let's build Apps",
	"tags": ["smartlearning", "Marketing", "Developer"],
	"members": ["ChrisVoiloe2", "InspireZim", "ShineOn"],
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["ChrisVoiloe2", "VictorPoseZw", "AnnaSmith"],
	"conversations": [
	{
	"chatId": 101,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe2",
	"comments": [
	{"user": "VictorPoseZw", "text": "Excited to write!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "AnnaSmith", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	}
	],
	"created_at": "2025-10-20T08:00:00Z"
	},
	{
	"id": 7,
	"name": "Tech Founders",
	"author": "VictorPoseZw",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Marketing", "Designer"],
	"members": ["VictorPoseZw", "DevKing", "CodeQueen"],
	"conversations": [
	{
	"chatId": 102,
	"title": "Startup Ideas",
	"author": "VictorPoseZw",
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["LegalBoss", "VictorPoseZw", "Admin1"],
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["ChrisVoiloe2", "InspireZim", "ShineOn"],
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
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["ChrisVoiloe2", "VictorPoseZw", "AnnaSmith"],
	"conversations": [
	{
	"chatId": 101,
	"title": "Kickoff Meeting",
	"author": "ChrisVoiloe2",
	"comments": [
	{"user": "VictorPoseZw", "text": "Excited to write!", "timestamp": "2025-10-22T10:00:00Z"},
	{"user": "AnnaSmith", "text": "Let's go!", "timestamp": "2025-10-22T10:05:00Z"}
	]
	}
	],
	"created_at": "2025-10-20T08:00:00Z"
	},
	{
	"id": 12,
	"name": "Tech Founders",
	"author": "VictorPoseZw",
	"members": ["VictorPoseZw", "DevKing", "CodeQueen"],
	"conversations": [
	{
	"chatId": 102,
	"title": "Startup Ideas",
	"author": "VictorPoseZw",
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["LegalBoss", "VictorPoseZw", "Admin1"],
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
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
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Marketing", "Designer"],
	"members": ["ChrisVoiloe2", "InspireZim", "ShineOn"],
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
	