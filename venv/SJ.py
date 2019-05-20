db.tweet.find({'retweet_count' : {$gt : 0}}, {_id:0, text:1, 'retweet_count':1})
db.tweet.find({retweet_count : {$eq : 0}})

db.tweet.find( { $and: [ { lang: "en" }, { 'place.name': {$in : ["United Kingdom", "Madrid"]} } ] }, {_id:0,lang:1,  'place.name':1} )

db.tweet.find({},{_id:0, 'user.friends_count':1, 'user.followers_count':1,'user.verified':1})

db.tweet.aggregate({$group : {_id : "$user.location", count : {$sum : 1}}},{$sort: {count : -1}})


db.tweet.aggregate({$group : {_id : "$place.name", count : {$sum : 1}}},{$sort: {count : -1}})


db.tweet.find({'user.location' : {$ne : null}},{_id:0, 'user':1}).limit(1)


#user의 계정이 검증되었고, statuses_count(작성한 트윗) 개수가 100000개 이상인 트윗의 text를 보여준다.
db.tweet.find({$and : [{'user.verified' : true},{'user.statuses_count' : {$gte : 100000}}]},{_id:0,'user.verified':1, 'user.statuses_count':1})

# place 객체가 null이 아닌 트윗들의 place 필드를 보여준다.
db.tweet.find({'place' : {$ne : null}},{_id:0, 'place':1})

# 엔티티 필드의 해시태그 개수가 세 개 이상이거나 url 개수가 네 개 이상인 트윗들의 엔티티.해시태그, 엔티티.url 필드를 보여준다.
db.tweet.find( { $or: [ {$where : 'this.entities.hashtags.length >= 3'}, {$where : 'this.entities.hashtags.length >= 4'} ] }, {_id:0,'entities.hashtags':1, 'entities.urls':1} )


db.tweet.find( {$where : { $or : [{'this.entities.hashtags.length >= 3'}, {'this.entities.urls.length >= 4'} ]} }, {_id:0,'entities.hashtags':1, 'entities.urls':1} )


# Find the tweets which do not written in 'en' and Tweet has been Retweeted is false and length of hashtags is grater than 3,
# Display the field`s entities.hashtags, lang, retweeted
db.tweet.find({$and:[{"lang" : {$ne :"en"}}, {"retweeted" : false}, {$where : "this.entities.hashtags.length > 3"}]}, {_id:0,'entities.hashtags':1, lang:1, retweeted:1})

# Find the tweets which place`s name is 'Madrid' and contain 'Real' for its user`s screen_name regardless of case. ,
# Display the field`s place.nave, user.screen_name
db.tweet.find({$or:[{"place.name" : 'Madrid'}, { "user.screen_name" : {$regex : 'Real', $options : 'i'}}]}, {_id:0,'place.name':1, 'user.screen_name':1})

# Combination of A, B and $match
# Find the tweets which entities`s hashtags.text or user`s screen name contains 'Real' for each's regardless of case and user`s followers count is greater than 500,000
db.tweet.aggregate({$match : {$and : [{$or : [{"entities.hashtags.text" : {$regex : "Liverpool", $options : "i"}},{"user.screen_name" : {$regex : "Liverpool", $options : "i"}}]}, {"user.followers_count" : {$gt : 500000}}]}})

#Display the fields user’s friends count, followers count, verified
# Fine the verified user`s tweet and display fields of user`s verified and screen_name
db.tweet.aggregate({$match : {"user.verified" : true}},{$project : {_id:0, "user.verified" : 1, "user.screen_name":1}})



db.tweet.aggregate({$unwind : "$hashtags"}, {$group : {_id : }})

# Show the count of each hashtags`s text, where a result sorted by the count
db.tweet.aggregate({$unwind : "$entities.hashtags"}, {$group : {_id : "$entities.hashtags.text", count : {$sum : 1}}},{$project : {_id :1, "count" : 1}}, {$sort : {"count" : -1}})


db.tweet.aggregate({$unwind : "$entities.hashtags"}, {$group : {_id : "$entities.hashtags.text", count : {$sum : 1}}},{$project : {_id :1, "count" : 1}}, {$sort : {"count" : -1}})

# Find the tweets which user`s followers count is greater than 10000 and user`s location is not null,
# and Show the count of each user`s location, where a result sorted by the count
db.tweet.aggregate({$match : {$and : [{"user.followers_count" : {$gt : 10000}}, {"user.location" : {$ne : null}}]}}, {$group : {_id : "$user.location", count : {$sum : 1}}}, {$sort : {"count" : -1}})

# First, unwind the entities.hasgtags, and Show the more than 6 count and hashtag`s texts of each tweet, result sorted by the count
# Find the tweets which user`s followers count is greater than 10000 and user`s location is not null,
# and Show the count of each user`s location, where a result sorted by the count
    db.tweet.aggregate({$unwind : "$entities.hashtags"}, {$group : {_id : "$id", hashtags : {$addToSet : "$entities.hashtags.text"}, count : {$sum : 1}}}, {$match : {count : {$gte : 6}}},
{$sort : {"count" : 1}})
