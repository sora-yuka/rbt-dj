r:
	./manage.py runserver
m:
	./manage.py makemigrations
	./manage.py migrate
c:
	./manage.py createsuperuser
f:
	./manage.py loaddata fixtures/users.json
	./manage.py loaddata fixtures/categories.json
	./manage.py loaddata fixtures/offers.json
	./manage.py loaddata fixtures/deals.json
