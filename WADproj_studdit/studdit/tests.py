    from django.test import TestCase
    from studdit.models import Post, Course, Student, Comment,User
    from django.db import transaction

    # Create your tests here.
    class CourseMethodTests(TestCase):
        def test_max_length(self):
            course = Course(code = "CS1PXTR", title = "A really really really really really really long course name that should hopefully exceed the max length")
            course.save()
            
            self.assertFalse(Course.objects.filter(code="CS1PX").exists())


    class IndexViewTests(TestCase):

        def starting(self):
            self.client=Client()
            self.user =User.objects.create_user(username='testuser', password='12345')
            self.course1 =Course.objects.create(name='Course 1', desc='This is course 1')
            self.course2 =Course.objects.create(name='Course 2', desc='This is course 2')

        def testLogin(self):
            self.client.login(username='eric', password='EricPass12')
            feedback = self.client.get(reverse('home'))
            self.assertEqual(response.status_code,200)

        def testCoursesShowUp(self):
            self.client.login(username='eric', password='EricPass12')
            response = self.client.get(reverse('home'))
            self.assertEqual(list(response.context['courses']), [self.course1, self.course2])


        def testInheritBase(self):
            home = self.tostring('home.html')
            base = self.tostring('base.html')

            self.assertIn(base, home)

        def tostring(self, temName):
            response = self.client.get(f'/{temName}/')
            return response.content.decode('utf-8')
        
        


    class PostMethodTests(TestCase):
        def test_upvotes(self):
            course = Course(code = "CS1PXTR", title = "CS")
            course.save()
            
            user = User.objects.create_user(username='john',email='jlennon@beatles.com',password='glass onion')
            user.save()
            student = Student(user = user)
            student.save()
            post = Post(course = course, post_author = student)
            post.upvotes = post.upvotes + 1
            self.assertEqual(post.upvotes, 1)
        
        def test_downvotes(self):
            course = Course(code = "CS1PXTR", title = "CS")
            course.save()
            
            user = User.objects.create_user(username='john',email='jlennon@beatles.com',password='glass onion')
            user.save()
            student = Student(user = user)
            student.save()
            post = Post(course = course, post_author = student)
            post.downvotes = post.downvotes + 1
            self.assertEqual(post.downvotes, 1)
        
        def test_user_can_only_upvote_once(self):
            course = Course(code = "CS1PXTR", title = "CS")
            course.save()
            
            user = User.objects.create_user(username='john',email='jlennon@beatles.com',password='glass onion')
            user.save()
            student = Student(user = user)
            student.save()
            post = Post(id = 1, course = course, post_author = student)
            post.save()
            post.upvotes = post.upvotes + 1
            post.upvoted_by.add(user)
            
            if post.upvoted_by.filter(id = 1).exists():
                pass
            else:
                post.upvotes = post.upvotes + 1
            self.assertEqual(post.upvotes, 1)
        
        def test_user_can_only_downvote_once(self):
            course = Course(code = "CS1PXTR", title = "CS")
            course.save()
            
            user = User.objects.create_user(username='john',email='jlennon@beatles.com',password='glass onion')
            user.save()
            student = Student(user = user)
            student.save()
            post = Post(id = 1, course = course, post_author = student)
            post.save()
            post.downvotes = post.downvotes + 1
            post.downvoted_by.add(user)
            
            if post.downvoted_by.filter(id = 1).exists():
                pass
            else:
                post.downvotes = post.downvotes + 1
            self.assertEqual(post.downvotes, 1)

    class CommentTests(TestCase):
        def test_unique_comment(self):
            course = Course(code = "CS1PXTR", title = "CS")
            course.save()
            
            user1 = User.objects.create_user(username='john',email='jlennon@beatles.com',password='glass onion')
            user1.save()
            student1 = Student(user = user1)
            student1.save()
            user2 = User.objects.create_user(username='jake',email='pmccarteny@beatles.com',password='glass apple')
            user2.save()
            student2 = Student(user = user2)
            student2.save()
            post = Post(course = course, post_author = student1)
            post.save()

            comment = Comment(post = post, student = student1, content = "do not repeat!")
            comment.save()
            try:
                with transaction.atomic():
                    comment2 = Comment(post = post, student = student2, content = "do not repeat!")
                    comment2.save()
            except:
                self.assertFalse(Comment.objects.filter(student = student2).exists())