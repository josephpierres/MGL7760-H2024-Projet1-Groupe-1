TIMES=1
for i in $(eval echo "{1..$TIMES}")
do
    siege -c 1 -r 10 http://localhost:8000/
    siege -c 3 -r 5 http://localhost:8000/getBookByAuthor
    siege -c 2 -r 5 http://localhost:8000/getBooksByCategory
    siege -c 5 -r 3 http://localhost:8082/getBooksByCategory/1
    siege -c 2 -r 10 http://localhost:8000/getBookByAuthor
    siege -c 2 -r 3 http://localhost:8082/getBooksByAuthor/h
    siege -c 1 -r 1 http://localhost:8082/getBooksByTitle/h
    sleep 5
done
