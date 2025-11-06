def get_suggestions():
    skills = [
    "Frontend", "Backend", "DevOps", "Marketing", "Finance", "Legal", "Real estate", "Bookkeeping", "Animation", "Video editing", "Data analysis",
    "Teaching", "Nursing", "Medicine", "Sports Coaching", "Music Performance", "Graphic Design", "Photography", "Digital Art", "Illustration",
    "Content Writing", "Copywriting", "Technical Writing", "Blogging", "Journalism", "Project Management", "Sales", "Customer Service", "Entrepreneurship",
    "Cloud Computing", "Data Science", "Machine Learning", "Cybersecurity", "Network Administration", "Database Administration", "Web Development", "UI/UX Design",
    "Yoga Instruction", "Dance", "Theater", "Painting", "Sculpture", "Event Planning", "Human Resources", "Recruitment", "Supply Chain Management", "Logistics",
    "Agriculture", "Horticulture", "Veterinary Care", "Dentistry", "Pharmacy", "Physical Therapy", "Occupational Therapy", "Speech Therapy", "Nutrition",
    "Culinary Arts", "Baking", "Pastry", "Interior Design", "Fashion Design", "Architecture", "Landscape Architecture", "Urban Planning", "Environmental Science",
    "Biotechnology", "Chemistry", "Physics", "Mathematics", "Statistics", "Economics", "Business Administration", "Public Administration", "Non-Profit Management"
    "Photography", "Videography", "Film Production", "Journalism", "Broadcasting", "Public Relations", "Communication", "Digital Marketing", "Social Media Management"
    ]
    return skills
    
def get_all_users():
    users = [
    {
    "id": 1,
    "name": "Dimond",
    "full_name": "Dimond Madechawo",
    "description": "A well known software dev.",
    "website": "http://smartlearning.liveblog365.com",
    "second_website": "github.com/dimondkudzai",
    "email": "diamondkudzai70@gmail.com",
    "confirm_email": True,
    "phone": "012 345 6789",
    "password": "chimboza@1",
    "image" : "image1.png",
    "skills": ["Health","Finance","Farmer","Software developer"],
    "clusters_count" : 7,
    "created_clusters": [1,2,7,12,4,1],
    "clusters_requests": [1,2,7,6,9,4,5],
    "notifications_count" : 4,
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
    "description": "A passionate designer",
    "website": "diamondkudzai70@gmail.com",
    "second_website": "github.com/dimondkudzai",
    "email": "contact@secoggnduser.co.za",
    "confirm_email": True,
    "phone": "+2712 345 6790",
    "password": "chimboza@1",
    "image" : "image2.png",
    "skills": ["Designer","Creativity"],
    "clusters_count" : 9,
    "created_clusters": [13,6,7,12,14,1],
    "clusters_requests": [10,6,7,6,9,4,5],
    "notifications_count" : 10,
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
    "second_website": "github.com/dimondkudzai",
    "email": "contact@seconduser.co.za",
    "confirm_email": True,
    "phone": "+2712 345 6790",
    "password": "chimboza@1",
    "image" : "image3.png",
    "skills": ["Public Speaking","Motivator","Counceling"],
    "clusters_count" : 9,
    "notifications_count" : 8,
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
    "second_website": "clustershub.co.zw/VictorPoseZw",
    "email": "contact@seconfghduser.co.za",
    "confirm_email": True,
    "phone": "012 345 6790",
    "password": "chimboza@1",
    "image" : "image4.png",
    "skills": ["Real estate","Construction","Legal"],
    "clusters_count": 0,
    "created_clusters": [10,6,7,1,14,5],
    "clusters_requests": [1,6,7,12,4,5],
    "notifications_count" : 4,
    "location": "USA",
    "messages":["@Dimond said something","We expect more","we will get there"]
    
    },
    {
    "id": 5,
    "name": "KnosiDubeSA",
    "full_name": "Knosilazi Dube",
    "description": "A lawyer in SA.",
    "second_website": "clustershub.co.zw/VictorPoseZw",
    "website": "www.sgueconduser.co.za",
    "email": "contact@setcondghuser.co.za",
    "confirm_email": True,
    "phone": "+26312 345 6790",
    "password": "chimboza@1",
    "image" : "image5.png",
    "skills": ["Marketing","Business","Analysis"],
    "clusters_count" : 1,
    "created_clusters": [1,6,7,12,14,15],
    "clusters_requests": [10,6,7,2,4,5],
    "notifications_count" : 3,
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
	"status": "Brain Flow AI",
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
	"created": "2025-10-22T10:00:00Z",
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
	"name": "Fish Farmers",
	"target": "Produce Breams for sale",
	"status": "Brain Flow AI",
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
	"created": "2025-10-22T10:00:00Z",
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
	"created": "2025-10-22T10:00:00Z",
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
	"status": "Brain Flow AI",
	"author": "Dimond",
	"created": "2025-10-22T10:05:00Z",
	"description": "Legal Firm",
	"target": "Fairness to everyone",
	"tags": ["legal", "marketing"],
	"members": ["Dimond", "VictorPoseZw"],
	"location": "Zimbabwe",
	"conversations": [
	{
	"chatId": 1,
	"title": "Welcome onboard",
	"author": "Dimond",
	"created": "2025-10-22T10:00:00Z",
	"comments": [
	{"user": "Admin1", "text": "We should meet next week.", "timestamp": "2025-10-20T09:00:00Z"}
	]
	}
	],
	"created": "2025-10-15T14:45:00Z",
	"requests": [
	{
	"chatId": 1,
	"title": "known devloper",
	"body": "Let me join i bring tidings.",
	"author": "Dimond",
	"created": "2025-10-22T10:00:00Z",
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
	"id": 4,
	"name": "Design Lab",
	"location": "Panama",
	"status": "Brain Flow AI",
	"author": "ChrisVoiloe2",
	"created": "2025-10-22T10:05:00Z",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Legal", "Co-founders", "DevOps"],
	"target": "Let's Design Apps",
	"members": ["AnnaSmith", "SketchMaster", "PixelHero"],
	"conversations": [
	{
	"chatId": 1,
	"title": "Color Theory",
	"author": "AnnaSmith",
	"created": "2025-10-22T10:00:00Z",
	"comments": [
	{"user": "SketchMaster", "text": "Love this topic!", "timestamp": "2025-10-18T11:30:00Z"}
	]
	}
	],
	"created": "2025-10-16T07:00:00Z",
	"requests": [
	{
	"chatId": 1,
	"title": "known devloper",
	"body": "Let me join i bring tidings.",
	"author": "Dimond",
	"created": "2025-10-22T10:00:00Z",
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

	
	]
	return clusters
	