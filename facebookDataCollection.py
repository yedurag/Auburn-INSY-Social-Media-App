
import urllib2
import json
import csv
import datetime

#Simple code to collect facebook posts and comments in a csv

 
def create_post_url(graph_url, APP_ID, APP_SECRET): 
    #create authenticated post URL
    post_args = "/posts/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
    post_url = graph_url + post_args
 
    return post_url
    
def render_to_json(graph_url):
    #render graph url call to JSON
    web_response = urllib2.urlopen(graph_url)
    readable_page = web_response.read()
    json_data = json.loads(readable_page)
    
    return json_data
 
def scrape_posts_by_date(graph_url, date, post_data, APP_ID, APP_SECRET):
    #render URL to JSON
    page_posts = render_to_json(graph_url)
    
    #extract next page
    if "paging" in page_posts.keys():
        if "next" in page_posts["paging"].keys():
            next_page = page_posts["paging"]["next"]
        else:
            next_page = ""
    else:
        next_page = ""
        
        
    
    #grab all posts
    page_posts = page_posts["data"]
    
    #boolean to tell us when to stop collecting
    collecting = True
    
    #for each post capture data
    for post in page_posts:
        try:
            
            current_post = [post["id"].encode('utf-8'), post["message"].encode('utf-8'),post["created_time"].encode('utf-8')]        
                            
        except Exception:
            current_post = [ "error", "error", "error"]
            
        if current_post[2] != "error":

            
            post_data.append(current_post)
            
            
    
    
    #If we still don't meet date requirements, run on next page            
    if collecting == True:
        if next_page != "":
            scrape_posts_by_date(next_page, date, post_data, APP_ID, APP_SECRET)
        
    
    
    return post_data
        
def get_likes_count(post_id, APP_ID, APP_SECRET):
    #create Graph API Call
    graph_url = "https://graph.facebook.com/" 
    likes_args = post_id + "/likes?summary=true&key=value&access_token" + APP_ID + "|" + APP_SECRET
    likes_url = graph_url + likes_args
    likes_json = render_to_json(likes_url)
 
    #pick out the likes count
    count_likes = likes_json["summary"]["total_count"]
 
    return count_likes



def create_comments_url(graph_url, post_id, APP_ID, APP_SECRET):
    #create Graph API Call
    comments_args = post_id + "/comments/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
    comments_url = graph_url + comments_args
    
    return comments_url

def get_comments_data(comments_url, comment_data, post_id):
    #render URL to JSON
    comments1 = render_to_json(comments_url)
    comments = comments1["data"]
    #for each comment capture data
    for comment in comments:
        try:
            current_comments = [comment["id"].encode('utf-8'), comment["message"].encode('utf-8') ,comment["created_time"].encode('utf-8'), post_id]
            
            comment_data.append(current_comments)
            
        except Exception:
            current_comments = ["error", "error", "error", "error"]
            
            
    #check if there is another page
    try:
        #extract next page
        next_page = comments1["paging"]["next"]
    except Exception:
        next_page = None
            
            
    #if we have another page, recurse
    if next_page is not None:
        get_comments_data(next_page, comment_data, post_id)
    else:
        return comment_data



def main():
    #simple data pull App Secret and App ID
    APP_SECRET = "ef5d6dc05fedba4f54508fc522285982"
    APP_ID = "1670164576554241"
    
    #to find go to page's FB page, at the end of URL find username
    #e.g. http://facebook.com/walmart, walmart is the username
    list_pages = ["T2Diabetes"]
    graph_url = "https://graph.facebook.com/"
    
    #the time of last weeks crawl
    last_crawl = datetime.datetime.now() - datetime.timedelta(weeks=10)
    last_crawl = last_crawl.isoformat()

    
    for page in list_pages:
        #make graph api url with company username
        current_page = graph_url + page
        
        #extract post data
        post_url = create_post_url(current_page, APP_ID, APP_SECRET)
        
        post_data = []
        
        post_data = scrape_posts_by_date(post_url, last_crawl, post_data, APP_ID, APP_SECRET)
        for post in post_data:
            post.append(page)
        comment_data = []
        all_comments = []
        #loop through and insert data
        for post in post_data:
        
            comment_url = create_comments_url(graph_url, post[0], APP_ID, APP_SECRET)
            comments = get_comments_data(comment_url, comment_data, post[0])

            if comments == None:
                comments = [["None","None","None",post[0]]]
            for comment in comments:
                all_comments.append(comment)
                
        
            

           
    
    
        
    
         

        
    
        f = open("output.csv", "wb")
        writer = csv.writer(f,delimiter='`')
        writer.writerow(['post_id','post_message', 'post_created_time'])
        for item in post_data:
            writer.writerow(item)
        f.close()
        print "done"
    
        f1 = open("outputcomments.csv", "wb")
        writer1 = csv.writer(f1,delimiter='`')
        writer1.writerow(['comment_id','comment_message', 'comment_created_time','post_id'])
        for item in all_comments:
            writer1.writerow(item)
        f1.close()
        print "donecomments"
    
if __name__ == "__main__":
    main()
