def get_all_backups():
    backups = [
    {
    "id": 1,
    "last_updated": "2026-01-01 00:00:00"
     }
     ]
    return backups
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
    "description": "Software developer.",
    "website": "http://smartlearning.liveblog365.com/dimond",
    "second_website": "https://github.com/dimondkudzai",
    "email": "diamondkudzai70@gmail.com",
    "confirm_email": True,
    "phone": "+263783702724",
    "password": "chimboza@1",
    "password_recovery": "chimboza",
    "image" : "image1.png",
    "member_clusters": [],
    "joined": "2025-12-12T14:30:00.000000",
    "skills": ["Farmer","Software developer"],
    "clusters_count" : 1,
    "created_clusters": [1,2,3,4],
    "clusters_requests": [1],
    "notifications_count" : 4,
    "location": "Zimbabwe",
    "messages":[{
    "id": 1,
    "body": "Hello mr CEO: 'Glad to have you!'",
    "read": False,
    "timestamp": "2025-12-12T14:30:00.000000",
    }]
    },
    
    ]
    return users
    
def get_all_clusters():
	clusters = [
	{
	"id": 1,
	"name": "Brain Flow AI",
	"status": "In progress",
	"target": "Building AI that solves health issues",
	"author": 2,
	"created": "2025-10-12T14:30:00.000000",
	"location": "International",
	"description": "Brain Flow AI is a project that aims to develop AI tools that reads brain flow data. This brain data will be recorded, analyzed and used for medical treatment eg Stroke, Stress, and Rehab. Github project https://github.com/BrainFlowAi/BrainFlowAi.",
	"tags": ["ML", "AI", "Neurology","health"],
	"members": [1,2],
	"updates": [{
	"message": "Cluster created by author",
	"timestamp": "2025-11-12T14:30:00.000000"
	}
	],
	"conversations": [
	{
	"chatId": 1,
	"title": "Looking for early contributors",
	"author": 1,
	"body": "Lets start working guys",
	"created": "2025-09-12T14:30:00.000000",
	"comments": [
	{"user": 1, "comment_id": 1, "text": "Excited to contribute!", "timestamp": "2025-09-12T14:30:00.000000"},
	{"user": 2,"comment_id": 2, "text": "Let's go!", "timestamp": "2025-09-12T14:30:00.000000"}
	]
	},
	],
	"requests": [
	{
	"chatId": 1,
	"title": "Testing requests",
	"body": "Let me join i bring tidings.",
	"author": 1,
	"created": "2025-09-12T14:30:00.000000",
	"comments": [
	{
	"user": 1,
	"comment_id": 1,
	"text": "Yes sure",
	"timestamp": "2025-09-12T14:30:00.000000"
	},

	]
	}
	]
	},
	{
	"id": 2,
	"name": "Fish Farmers",
	"target": "Produce Breams for sale",
	"status": "Idea",
	"author": 2,
	"created": "2025-11-12T14:30:00.000000",
	"location": "Zimbabwe",
	"members": [1,2],
	"updates": [{
	"message": "Cluster created",
	"timestamp": "2025-11-12T14:30:00.000000"
	},
	],
	"description": "Fish production is cheap and there is market in Zimbabwe. With land and small capital much returns",
	"tags": ["Farmer", "Marketing", "Finance"],
	"conversations": [
	{
	"chatId": 1,
	"title": "For Starting",
	"body": "Let's find land with dam or pond.",
	"author": 1,
	"created": "2025-11-13T14:30:00.000000",
	"comments": [
	{
	"user": 1,
	"comment_id": 2,
	"text": "Yes sure",
	"timestamp": "2025-09-12T14:30:00.000000"
	},
	]
	}
	],
	"requests": [
	{
	"chatId": 1,
	"title": "Im a well known devloper",
	"body": "Let me join i bring tidings.",
	"author": 1,
	"created": "2025-09-12T14:30:00.000000",
	"comments": [
	{
	"user": 1,
	"text": "Yes sure",
	"timestamp": "2025-09-12T14:30:00.000000",
	"comment_id": 2,
	},
	
	]
	}
	]
	
	},
	{
	"id": 3,
	"name": "Legal Minds",
	"status": "In progresss",
	"author": 2,
	"created": "2025-12-12T14:30:00.000000",
	"description": "Legal Firm",
	"target": "Fairness to everyone",
	"tags": ["legal", "marketing"],
	"members": [1,2],
	"updates": [{
	"message": "Created by author",
	"timestamp": "2025-12-12T14:30:00.000000"
	},

	],
	"location": "Zimbabwe",
	"conversations": [
	{
	"chatId": 1,
	"title": "Welcome onboard",
	"author": 1,
	"created": "2025-11-12T14:30:00.000000",
	"comments": [
	{"user": 1, "comment_id": 2,"text": "We should meet next week.", "timestamp": "2025-09-12T14:30:00.000000"}
	]
	}
	],
	"created": "2025-11-12T14:30:00.000000",
	"requests": [
	{
	"chatId": 1,
	"title": "Im a well known lawyer",
	"body": "Let me join i bring tidings.",
	"author": 1,
	"created": "2025-11-12T14:30:00.000000",
	"comments": [
	{
	"user": 1,
	"comment_id": 2,
	"text": "Yes sure",
	"timestamp": "2025-11-12T14:30:00.000000"
	},
	{
	"user": 1,
	"text": "Let's go!",
	"comment_id": 2,
	"timestamp": "2025-11-12T14:30:00.000000"
	}
	]
	}
	]
	},
	{
	"id": 4,
	"name": "Design Lab",
	"location": "Panama",
	"status": "Idea",
	"author": 2,
	"created": "2025-11-12T14:30:00.000000",
	"location": "Harare",
	"description": "Buiding Everything",
	"tags": ["Co-founders", "DevOps"],
	"target": "Let's Design apps and softwares.",
	"members": [1,2],
	"updates": [{
	"message": "Thank you for joining",
	"timestamp": "2025-11-12T14:30:00.000000"
	},
	{
	"message": "You know good on you is for joining",
	"timestamp": "2025-11-12T14:30:00.000000"
	}
	],
	"conversations": [
	{
	"chatId": 1,
	"title": "Lets get started",
	"author": 1,
	"created": "2025-11-12T14:30:00.000000",
	"comments": [
	{"user": 1, "comment_id": 2,"text": "Love this topic!", "timestamp": "2025-09-12T14:30:00.000000"}
	]
	}
	],
	"created": "2025-11-12T14:30:00.000000",
	"requests": [
	{
	"chatId": 1,
	"title": "known devloper",
	"body": "Let me join i bring tidings.",
	"author": 1,
	"created": "2025-11-12T14:30:00.000000",
	"comments": [
	{
	"user": 1,
	"comment_id": 2,
	"text": "Yes sure",
	"timestamp": "2025-11-12T14:30:00.000000"
	},
	{
	"user": 1,
	"text": "Let's go!",
	"comment_id": 2,
	"timestamp": "2025-11-12T14:30:00.000000"
	}
	]
	}
	]
	},

	
	]
	return clusters
	