To connect to aws
ssh -i oceanblues.pem ubuntu@ec2-52-88-9-177.us-west-2.compute.amazonaws.com

NOTE: You will need .pem file to connect. Contact me for the file.

In the cloud git project is cloned under swm-amazon folder.


ToDo:
-Retrieve data from the website for 
	- Index
	- Most helpful customer reviews (done)
	- Customer Reviews
-Add postgresql
-come up with schema and tables
-write data to DB


'Files to look into'
ProductListScraper takes the url of product list under a compnay and calls ProductPageReviewScraper for each product.