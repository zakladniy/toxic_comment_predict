# toxic-comment-predict

Simple Web-API based on FastAPI and deployed on Heroku service.

This Web-service provide to predict toxic or non toxic russian comments based on BERT model

## Try Web application
https://russian-toxic-comment-predict.herokuapp.com/


## How to run application?
Clone repo:
  ```console 
    https://github.com/zakladniy/toxic_comment_predict.git
  ```

### With poetry
Check poetry in you OS

Install with poetry
  ```console 
    poetry install
  ```

Activate env
  ```console 
    poetry shell
  ```

Run with:
  ```console 
    make run
  ```
### With docker

Create image:
  ```console 
    sudo docker build -t toxic_comment .
  ```
Run container:
  ```console 
    sudo docker run -p 80:80 -d toxic_comment
  ```
Open in browser url:
  ```console 
    http://127.0.0.1/docs
  ```

## Screenshots of application
### Common view
![](https://github.com/zakladniy/toxic_comment_predict/blob/main/screenshots/common_view_new.png)

### Request
![](https://github.com/zakladniy/toxic_comment_predict/blob/main/screenshots/request.png)

### Response
![](https://github.com/zakladniy/toxic_comment_predict/blob/main/screenshots/response.png)