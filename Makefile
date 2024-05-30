docker-build:
	docker build ./ -t hair_color_recommender

docker-run:
	docker run -p 7860:7860 --name hair_color_recommender_1 hair_color_recommender 

docker-start:
	docker start hair_color_recommender_1

docker-stop:
	docker stop hair_color_recommender_1