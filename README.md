# Linguisage Dictionary 

This is a microservice responsible for storing and managing words, 
along with all related information such as senses, examples, images, 
and more.


1. **Swagger Interactive Documentation**: Explore detailed descriptions for all endpoints at `/docs`.

2. **Admin Panel**: A user-friendly interface for management and monitoring at `/admin`.

3. **Background Task for Missing Words**:

   - If a word is not found in the dictionary, a Celery background task is initiated.
   - This task attempts to parse information and images for the missing word.
   - Tasks are stored in Redis.
   - View ongoing tasks in the user-friendly Flower GUI interface at port `5555`.