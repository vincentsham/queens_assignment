# Queen's Assignment
Temporary link of the website: http://138.197.129.191/main/

## Usage
To start the website on local host
```
python3 __init__.py
```
## Requested Features
The website shows the top ten newest Android-related questions and the top 10 most voted Android-related questions. In the navigation bar, users can switch the view of the newest questions or the most voted questions. Users can click on the questions, and then the content and replies will pop up below. Users can re-click the questions to hide the details.


## New Features
1. I implemented a filter bar that allows users to type in keywords to filter the questions.
2. I implemented a simple backend application to notify me if the website has any errors via email.
```
nohup python3 notification.py sender receiver password logfile &
```

## Future Improvements
1. Web scraping is slow due to the latency of tons of requests and responses, which is unavoidable. Making good use of multiprocessing and threading would be one of the ways for mitigating this issue.
2. For making the website more interactive with StackOverflow, I would like to use StackOverflow API that allows users to login via OAuth for voting and replying, etc..
3. One of the main problems in StackOverflow is to have many duplicated questions. Even though StackOverflow implemented a great algorithm to find related past posts, it is still troublesome to keep seeing a lot of duplicated questions on the website or StackOverflow. We can try to implement our model to solve this issue. For unsupervised learning, word embedding plus VAE would learn a generative model. That may be useful to get related posts based on the distance of two posts on the latent variables' distribution. If we can collect data of accepted redirect posts, we can do supervised learning complementing with the latent variables of unsupervised learning and the state-of-art NLP process like transformer model. 
