import spacy
from collections import defaultdict, Counter
import PyPDF2
import docx
import sys
import json

# Load SpaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Load updated domain-specific keywords, certifications, and project ideas
DOMAIN_KEYWORDS = {
  'Software Engineering': {
    'keywords': {
        'python': 10, 'java': 9, 'c++': 8, 'javascript': 9, 'typescript': 8,
        'react': 8, 'node.js': 8, 'angular': 7, 'git': 9, 'docker': 8, 
        'kubernetes': 7, 'sql': 9, 'nosql': 8, 'aws': 8, 'azure': 7, 
        'data structures': 10, 'algorithms': 10, 'microservices': 8, 
        'rest api': 9, 'ci/cd': 8
    },
    'certifications': {
        'aws certified developer': 10, 'oracle java certification': 9, 
        'google professional cloud developer': 8, 'microsoft azure developer associate': 8, 
        'cisco certified devnet professional': 7
    },
    'project_ideas': {
        'personal expense tracker': 9, 'job portal with resume ranking': 8, 
        'chatbot for career guidance': 8, 'e-commerce website with recommendation system': 9, 
        'real-time collaborative code editor': 9, 'ai-powered document summarizer': 8, 
        'blockchain-based voting system': 9, 'ml-based fake news detection': 9, 
        'ai-powered code review system': 8, 'cloud-based file storage system': 9, 
        'intelligent chatbot for mental health': 8, 'network intrusion detection system': 9, 
        'iot-based home automation system': 8, 'ai-powered resume parser': 9, 
        'smart contract-based supply chain tracking': 8, 'face recognition-based attendance system': 8, 
        'peer-to-peer file sharing system': 9, 'real-time stock market prediction': 9, 
        'handwritten text recognition using deep learning': 8, 'customizable low-code development platform': 9
    }
},
 
'Data Science': {
    'keywords': {
        'python': 10, 'r': 9, 'tensorflow': 10, 'keras': 9, 'pandas': 10, 
        'numpy': 9, 'scikit-learn': 10, 'machine learning': 10, 'deep learning': 9, 
        'sql': 8, 'matplotlib': 8, 'seaborn': 8, 'data visualization': 9, 
        'nlp': 9, 'big data': 8, 'power bi': 8, 'hadoop': 7, 'spark': 8, 
        'cloud computing': 8, 'statistics': 9
    },
    'certifications': {
        'google data engineer': 10, 'ibm data science professional': 9, 
        'microsoft certified: azure data scientist': 8, 'tensorflow developer certificate': 9, 
        'aws certified machine learning specialty': 9
    },
    'project_ideas': {
        'customer churn prediction': 9, 'stock price prediction': 9, 
        'movie recommendation system': 8, 'sentiment analysis on social media': 9, 
        'fraud detection in banking': 10, 'medical image classification': 9, 
        'credit risk prediction': 9, 'automated resume screening': 8, 
        'text summarization using NLP': 9, 'speech-to-text converter': 8, 
        'real-time traffic prediction': 9, 'fake news detection': 9, 
        'chatbot for customer support': 8, 'house price prediction': 9, 
        'disease prediction using medical data': 9, 'video caption generator': 8, 
        'handwritten digit recognition': 9, 'real-time object detection': 9, 
        'anomaly detection in network traffic': 8, 'weather forecasting using ML': 9
    }
}
,


'Graphics Designing': {
    'keywords': {
        'photoshop': 10, 'illustrator': 10, 'indesign': 9, 'adobe xd': 8, 'figma': 10, 
        'ui/ux': 9, 'creativity': 8, 'branding': 9, 'canva': 8, 'typography': 9, 
        'color theory': 9, 'after effects': 8, 'premiere pro': 8, 'motion graphics': 9, 
        'digital painting': 8, '3d modeling': 7, 'vector graphics': 9, 'wireframing': 8, 
        'visual hierarchy': 9, 'storyboarding': 8
    },
    'certifications': {
        'adobe certified expert': 10, 'ux design certificate': 9, 
        'google ux design professional': 9, 'certified digital designer': 8, 
        'interaction design foundation certification': 8
    },
    'project_ideas': {
        'branding package for a startup': 9, 'poster design for an event': 8, 
        'mobile app UI design': 9, 'website UI/UX redesign': 9, 'social media post templates': 8, 
        'animated logo design': 9, 'business card & letterhead design': 8, 
        'infographic design': 9, 'ebook or magazine layout': 8, 'game UI/UX design': 9, 
        'motion graphics video': 9, '3D product mockup': 8, 'custom typography project': 9, 
        'illustration for a children’s book': 8, 'AR filters for Instagram/Snapchat': 8, 
        'brand mascot design': 9, 'interactive prototyping for apps': 9, 
        'storyboard for an animation': 8, 'packaging design for a product': 9, 
        'themed icon set creation': 8
    }
},


'AI ML': {
    'keywords': {
        'python': 10, 'machine learning': 10, 'deep learning': 10, 'pytorch': 9, 'tensorflow': 10, 
        'opencv': 8, 'nlp': 9, 'bert': 9, 'transformer': 9, 'reinforcement learning': 9, 
        'scikit-learn': 10, 'computer vision': 9, 'speech recognition': 8, 'GANs': 9, 
        'XGBoost': 9, 'data preprocessing': 8, 'feature engineering': 9, 'time series analysis': 8, 
        'model deployment': 9, 'autoML': 8
    },
    'certifications': {
        'tensorflow developer': 10, 'ai engineering certificate': 9, 
        'google professional ML engineer': 9, 'ibm AI engineering': 9, 
        'stanford ML specialization': 8
    },
    'project_ideas': {
        'image classification using CNN': 9, 'chatbot with NLP': 9, 
        'AI-based resume screening': 9, 'fraud detection system': 9, 'AI-powered recommendation system': 9, 
        'object detection with YOLO': 9, 'time series forecasting for stock prices': 9, 
        'voice assistant using speech recognition': 9, 'GANs for image generation': 9, 
        'self-learning AI using reinforcement learning': 9, 'fake news detection with NLP': 9, 
        'AI-driven sentiment analysis': 9, 'handwritten digit recognition': 8, 
        'autonomous driving simulation': 9, 'medical diagnosis using AI': 9, 
        'pose estimation with AI': 8, 'AI-powered content summarization': 9, 
        'AI-based question answering system': 9, 'AI for code generation and debugging': 9, 
        'anomaly detection in cybersecurity': 9
    }
},


'Application Support Engineer': {
    'keywords': {
        'linux': 9, 'sql': 9, 'scripting': 8, 'bash': 8, 'powershell': 7, 'jira': 7, 
        'incident management': 9, 'problem solving': 8, 'communication skills': 9, 
        'windows server': 8, 'monitoring tools': 8, 'troubleshooting': 9, 
        'log analysis': 8, 'ticketing systems': 8, 'cloud platforms (AWS/Azure)': 8, 
        'networking basics': 8, 'system administration': 8, 'serviceNow': 7, 
        'performance tuning': 8, 'IT security fundamentals': 8
    },
    'certifications': {
        'itil foundation': 10, 'microsoft certified azure administrator': 8, 
        'aws certified sysops administrator': 8, 'red hat certified system administrator (RHCSA)': 9, 
        'compTIA Linux+': 8
    },
    'project_ideas': {
        'automated system health monitoring tool': 9, 'log analysis and anomaly detection': 9, 
        'ticket management automation system': 8, 'custom server performance dashboard': 8, 
        'incident tracking and reporting tool': 8, 'automated database backup and recovery system': 9, 
        'cloud resource monitoring system': 8, 'AI-powered troubleshooting assistant': 9, 
        'custom alerting system for application errors': 8, 'real-time server health monitoring system': 9, 
        'configuration management tool using Ansible': 8, 'log aggregation and visualization dashboard': 9, 
        'security audit and compliance tracking system': 9, 'auto-scaling infrastructure deployment': 8, 
        'chatbot for IT support queries': 8, 'process automation using PowerShell and Bash': 9, 
        'custom reporting tool for IT incidents': 8, 'self-healing scripts for common application issues': 9, 
        'remote server access and troubleshooting tool': 8, 'performance benchmarking and analysis tool': 8
    }
},



'Project Management': {
    'keywords': {
        'project planning': 10, 'agile': 9, 'scrum': 9, 'risk management': 8, 'team leadership': 9, 
        'budget management': 8, 'stakeholder communication': 9, 'kanban': 8, 'jira': 8, 'time management': 9, 
        'resource allocation': 8, 'conflict resolution': 8, 'scope management': 9, 'process improvement': 8, 
        'change management': 9, 'performance tracking': 8, 'quality assurance': 8, 'strategic planning': 9, 
        'vendor management': 8, 'reporting and analytics': 8
    },
    'certifications': {
        'pmp': 10, 'prince2': 9, 'certified scrum master': 9, 'six sigma green belt': 8, 
        'agile certified practitioner (PMI-ACP)': 9
    },
    'project_ideas': {
        'AI-powered project risk assessment tool': 9, 'automated task prioritization system': 9, 
        'project cost estimation and tracking tool': 8, 'team performance analytics dashboard': 8, 
        'agile sprint planning and tracking system': 9, 'intelligent workload distribution tool': 8, 
        'stakeholder feedback and sentiment analysis tool': 8, 'automated meeting minutes and action items tracker': 9, 
        'Gantt chart-based project scheduling tool': 8, 'resource utilization optimization system': 9, 
        'Jira integration for automated project status reporting': 8, 'AI-driven deadline prediction model': 9, 
        'collaborative decision-making platform': 9, 'project portfolio management system': 8, 
        'risk management dashboard with historical data insights': 9, 'workflow automation for repetitive tasks': 9, 
        'employee performance and contribution tracking system': 8, 'predictive project budget forecasting tool': 9, 
        'time tracking and productivity enhancement tool': 8, 'personalized career progression planner for project managers': 8
    }
},



'Software Development': {
    'keywords': {
        'python': 10, 'java': 10, 'c#': 9, 'javascript': 9, 'html': 8, 'css': 8, 'git': 9, 'sql': 9, 
        'algorithms': 9, 'data structures': 9, 'api development': 8, 'microservices': 8, 'docker': 8, 
        'kubernetes': 7, 'design patterns': 8, 'testing': 9, 'cloud computing': 8, 'agile methodology': 9, 
        'version control': 9, 'software architecture': 8
    },
    'certifications': {
        'oracle java certification': 9, 'microsoft certified: azure developer associate': 9, 
        'aws certified developer': 9, 'google associate cloud engineer': 8, 'pmp (for software projects)': 7
    },
    'project_ideas': {
        'AI-based code review tool': 9, 'automated bug tracking system': 9, 'real-time collaborative code editor': 9, 
        'intelligent IDE plugin for debugging': 8, 'smart API documentation generator': 8, 
        'cloud-based CI/CD pipeline automation': 9, 'self-healing microservices system': 9, 
        'AI-powered chatbot for software development queries': 8, 'serverless application development framework': 9, 
        'dynamic load balancing for distributed systems': 8, 'code versioning analytics tool': 9, 
        'performance profiling and optimization tool': 8, 'developer productivity analytics system': 9, 
        'AI-driven automated testing framework': 9, 'interactive coding challenge platform': 9, 
        'cross-platform mobile app development framework': 8, 'intelligent bug prediction and prevention tool': 9, 
        'cloud-native development monitoring tool': 9, 'language-agnostic software dependency manager': 8, 
        'AI-enhanced refactoring assistant': 9
    }
},



'Computer Networking': {
    'keywords': {
        'network security': 9, 'tcp/ip': 10, 'dns': 9, 'dhcp': 8, 'switching': 9, 'routing': 9, 'firewalls': 9, 
        'vpn': 8, 'wireshark': 8, 'cisco ios': 9, 'bgp': 8, 'ospf': 9, 'network automation': 8, 'sdn': 8, 
        'load balancing': 8, 'ipv6': 9, 'snmp': 8, 'wireless networking': 8, 'network monitoring': 9, 
        'zero trust security': 8
    },
    'certifications': {
        'ccna': 10, 'network+': 9, 'ccnp': 9, 'cissp (network security focus)': 9, 'juniper jncia': 8
    },
    'project_ideas': {
        'network intrusion detection system': 9, 'vpn setup and security enhancement': 9, 'firewall rule optimization tool': 9, 
        'ai-based anomaly detection in network traffic': 9, 'automated network configuration management': 8, 
        'real-time packet analysis dashboard': 9, 'cloud-based network monitoring tool': 9, 'self-healing network system': 9, 
        'load balancer optimization tool': 8, 'wireless network penetration testing tool': 8, 
        'sdn-based dynamic network optimization': 9, 'cyber threat intelligence system': 9, 'ipv6 migration strategy': 8, 
        'zero-trust network architecture simulation': 9, 'network simulation tool with ai insights': 8, 
        'intelligent network topology mapper': 9, 'real-time dns attack mitigation system': 9, 
        'iot network security assessment tool': 8, 'data center network automation': 9, 'network performance prediction using ml': 9
    }
},




'Cyber Security': {
    'keywords': {
        'network security': 10, 'ethical hacking': 9, 'penetration testing': 9, 'firewalls': 9, 'ids/ips': 8, 
        'risk assessment': 8, 'vulnerability management': 9, 'cryptography': 9, 'incident response': 9, 'siem': 8, 
        'forensics': 9, 'malware analysis': 9, 'zero trust security': 8, 'cloud security': 9, 'secure coding': 8, 
        'reverse engineering': 8, 'phishing detection': 9, 'red teaming': 8, 'blue teaming': 8, 'iot security': 8
    },
    'certifications': {
        'ceh': 10, 'cissp': 9, 'comptia security+': 9, 'oscp': 10, 'gsec': 9
    },
    'project_ideas': {
        'automated vulnerability scanner': 9, 'ransomware detection system': 9, 'honeypot for intrusion detection': 9, 
        'ai-based phishing email detector': 9, 'secure file encryption tool': 9, 'cloud security monitoring dashboard': 9, 
        'penetration testing automation': 9, 'log analysis tool using siem': 9, 'zero trust architecture implementation': 9, 
        'network traffic anomaly detection using ml': 9, 'secure password manager': 8, 'malware behavior analysis tool': 9, 
        'social engineering awareness chatbot': 8, 'iot security threat detection system': 9, 'secure api gateway': 9, 
        'data breach detection and alert system': 9, 'cyber threat intelligence platform': 9, 
        'browser extension for detecting malicious sites': 8, 'blockchain-based identity management': 9, 
        'ai-driven cyber attack prediction tool': 9
    }
},




'Database Engineer': {
    'keywords': {
        'sql': 10, 'mysql': 9, 'postgresql': 9, 'oracle db': 9, 'nosql': 8, 'mongodb': 8, 'database design': 9, 
        'data modeling': 9, 'performance tuning': 8, 'backup and recovery': 9, 'query optimization': 9, 'etl': 8, 
        'indexing': 8, 'sharding': 8, 'replication': 9, 'stored procedures': 8, 'cassandra': 7, 'redis': 7, 
        'cloud databases': 9, 'database security': 9
    },
    'certifications': {
        'oracle certified professional (ocp)': 10, 'microsoft certified: azure database administrator': 9, 
        'aws certified database - specialty': 9, 'google professional data engineer': 9, 'mongodb certified developer': 8
    },
    'project_ideas': {
        'high-performance sql query optimizer': 9, 'database migration automation': 9, 'nosql vs sql performance comparison tool': 8, 
        'database load balancer': 9, 'real-time database monitoring system': 9, 'data warehouse implementation': 9, 
        'distributed database design for big data': 9, 'cloud-based database backup system': 9, 'database security audit tool': 9, 
        'etl pipeline for large-scale data processing': 9, 'automated database indexing tool': 8, 'mysql replication setup with failover': 9, 
        'graph database visualization system': 8, 'time-series database analysis': 9, 'data consistency checker for large datasets': 9, 
        'postgresql sharding implementation': 9, 'query caching mechanism for high-speed applications': 9, 
        'real-time event-driven database triggers': 9, 'ai-powered anomaly detection in databases': 9, 
        'log-based change data capture system': 9
    }
},
'Business Analysis': {
    'keywords': {
        'data analysis': 10, 'business intelligence': 9, 'sql': 9, 'excel': 10, 
        'power bi': 9, 'tableau': 9, 'market research': 8, 'financial modeling': 8, 
        'predictive analytics': 8, 'stakeholder management': 9, 'agile methodology': 9, 
        'scrum': 8, 'business process modeling': 9, 'requirements gathering': 9, 
        'user stories': 8, 'kpis & metrics': 9, 'dashboard creation': 9, 'data visualization': 9, 
        'crm': 8, 'erp systems': 8, 'swot analysis': 8, 'risk analysis': 8, 
        'business strategy': 9, 'cost-benefit analysis': 9, 'gap analysis': 8, 
        'use case modeling': 8, 'customer journey mapping': 8, 'lean six sigma': 8
    },
    'certifications': {
        'certified business analyst professional (cbap)': 10, 'pmp': 9, 
        'prince2': 8, 'agile certified practitioner (pmi-acp)': 9, 
        'tableau desktop specialist': 8, 'power bi data analyst associate': 8, 
        'certified scrum master (csm)': 8, 'six sigma green belt': 8
    },
    'project_ideas': {
        'customer segmentation analysis': 9, 'sales forecasting using data analytics': 9, 
        'market trend analysis dashboard': 8, 'crm data-driven insights system': 9, 
        'real-time financial risk assessment tool': 9, 'business process automation for retail': 8, 
        'supply chain optimization using analytics': 9, 'ai-powered business decision-making tool': 9, 
        'competitive analysis and pricing optimization': 8, 'predictive analytics for customer churn': 9, 
        'smart inventory management system': 9, 'revenue forecasting model': 9, 
        'automated financial statement analysis': 8, 'data-driven employee productivity analysis': 8, 
        'real-time customer sentiment analysis': 9, 'intelligent report generation tool': 8, 
        'customer lifetime value prediction': 9, 'automated compliance tracking system': 8, 
        'ai-powered contract analysis system': 8, 'data-driven HR analytics dashboard': 9
    }
}
}

PROJECT_BONUS_SCORE = 20  # Bonus points if a project related to the domain is found

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.lower()

# Extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return ' '.join([p.text for p in doc.paragraphs]).lower()

# Analyze keywords and assign scores
def analyze_keywords(text, input_domain):
    doc = nlp(text)
    word_freq = Counter([token.text for token in doc if not token.is_stop and not token.is_punct])
    score = 0
    hits = []
    
    if input_domain in DOMAIN_KEYWORDS:
        for keyword, weight in DOMAIN_KEYWORDS[input_domain]['keywords'].items():
            if keyword in word_freq:
                freq = word_freq[keyword]
                score += weight * freq
                hits.append(keyword)
        for cert, weight in DOMAIN_KEYWORDS[input_domain]['certifications'].items():
            if cert.lower() in text:
                score += weight * 2
                hits.append(cert)
    
    return score, hits

# Check if a relevant project is mentioned
def check_project_related_to_domain(text, input_domain):
    project_score = 0
    matched_projects = 0
    
    if input_domain in DOMAIN_KEYWORDS:
        for project, weight in DOMAIN_KEYWORDS[input_domain]['project_ideas'].items():
            if project.lower() in text:
                project_score += weight
                matched_projects += 1
            if matched_projects >= 5:  # Stop after 5 matches
                break
    
    return project_score

# Analyze resume and rank it out of 100
def analyze_resume(file_path, input_domain):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        return {'error': 'Unsupported file format. Please upload PDF or DOCX.'}

    score, found_skills = analyze_keywords(text, input_domain)
    project_score = check_project_related_to_domain(text, input_domain)
    score += project_score  # Add project score to total
    
    # Normalize score to be out of 100
    max_possible_score = sum(DOMAIN_KEYWORDS[input_domain]['keywords'].values()) * 5 + 50  # Including project score
    normalized_score = min(100, (score / max_possible_score) * 100)
    
    # Calculate rating (out of 10)
    rating = round((normalized_score / 100) * 10, 1)

    # Identify missing skills and projects
    all_keywords = set(DOMAIN_KEYWORDS[input_domain]['keywords'].keys())
    all_certs = set(DOMAIN_KEYWORDS[input_domain]['certifications'].keys())
    all_projects = set(DOMAIN_KEYWORDS[input_domain]['project_ideas'].keys())
    found = set(found_skills)
    missing = list((all_keywords | all_certs | all_projects) - found)
    
    return {
        'domain': input_domain,
        'score': round(normalized_score, 2),
        'rating': rating,  # Ensure rating is always included
        'found_skills': found_skills,
        'suggestions': missing if missing else ["None! Great resume!"]  # Ensure suggestions is always included
    }

# ---------- MAIN ----------
if __name__ == "__main__":
    file_path, input_domain = sys.argv[1], sys.argv[2]
    print(json.dumps(analyze_resume(file_path, input_domain), indent=4))
    
