from google.appengine.ext import ndb

from user import User
from post import Post

def getPosts(user, collection, images):
    generated_posts = []
    posts = getUserPost(user.posts)
    for post in reversed(posts):
        try:
            blob_index = collection.filenames.index(post.image)
            blob_id = collection.blobs[blob_index]
            images_url = images.get_serving_url(blob_id, secure_url=False)
        except:
            images_url = "https://pngimage.net/wp-content/uploads/2018/05/error-png-3.png"
        temp = {}
        temp["post"] = post
        temp["image_url"] = images_url
        generated_posts.append(temp)

    return generated_posts

def getUserPost(user_post):
    posts = []
    if len(user_post)<= 0:
        return posts
    else:
        for post_id in user_post:
            post = ndb.Key( 'Post', int(post_id) ).get()
            posts.append(post)
    return posts

def getImage(user, collection, images):
    if user:
        try:
            blob_index = collection.filenames.index(user.image_label)
            blob_id = collection.blobs[blob_index]
            return images.get_serving_url(blob_id, secure_url=False)
        except:
            return "https://cdn2.iconfinder.com/data/icons/user-icon-2-1/100/user_5-15-512.png"
    else:
        return "https://cdn2.iconfinder.com/data/icons/user-icon-2-1/100/user_5-15-512.png"

def getSelectedUserInstance(user_id):
    user = None
    user_list = User.query().fetch()
    for user_item in user_list:
        if user_id == str(user_item.key.id()):
            user = user_item
    return user

def getAccounts(user_id, search_string):
    all_accounts = User.query().fetch()
    if search_string == "":
        return getAllAccounttExceptCurrentAccount(all_accounts, user_id)
    return getFilterAccountList(all_accounts, user_id, search_string)

def getAllAccounttExceptCurrentAccount(all_accounts, user_id):
    accounts = []
    for acct in all_accounts:
        if str(acct.key.id()) != user_id:
            accounts.append(acct)
    return accounts

def getFilterAccountList(all_accounts, user_id, search_string):
    accounts = []
    for acct in all_accounts:
        if str(acct.key.id()) != user_id and str(search_string).lower() in str(acct.username).lower():
            accounts.append(acct)
    return accounts

def getFollowedStatus(following, user_id):
    followed = False
    for id in following:
            if user_id in id:
                followed = True
    return followed

def getCurrentUserTimelinePost(main_user):
    posts = []
    for user_id in main_user.following:
        for de_user in User.query().fetch():
            if str(de_user.key.id()) == user_id:
                user = ndb.Key( 'User', de_user.key.id() ).get()
                posts.extend(getUserPost(user.posts))
    posts.extend(getUserPost(main_user.posts))
    return posts

def sortPostByDateInDesendingOrder(posts):
    for index in range(len(posts)-1,0,-1):
        for idx in range(index):
            try:
                if posts[idx].created_at < posts[idx+1].created_at:
                    temp = posts[idx]
                    posts[idx] = posts[idx+1]
                    posts[idx+1] = temp
            except:
                pass
    return posts

def getFirstFiftyPostWithImages(posts, collection, images):
    selected_posts = []
    count = 0
    if len(posts) <= 50:
        count = len(posts)
    else:
        count = 50

    for index in range(count):
        try:
            blob_index = collection.filenames.index(posts[index].image)
            blob_id = collection.blobs[blob_index]
            images_url = images.get_serving_url(blob_id, secure_url=False)
        except:
            images_url = "https://pngimage.net/wp-content/uploads/2018/05/error-png-3.png"

        post_ownwer = getSelectedUserInstance(posts[index].owner_id)
        temp = {}
        temp["post"] = posts[index]
        temp["image_url"] = images_url
        temp["owner"] = str(post_ownwer.username).lower()
        temp["post_owner_profile_image"] = getImage(post_ownwer, collection, images)
        selected_posts.append(temp)
    return selected_posts

def getUserListFromFollowship(options):
    user_list = []
    for option in options:
        for item in User.query().fetch():
            if str(item.key.id()) == option:
                user_list.append(item)
    return user_list
