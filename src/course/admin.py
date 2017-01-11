from django.contrib import admin

from .models import Course, StudentCourse, Syllabus, Assignment, CourseNote

class CourseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'course_name', 'course_num', 'course_time', 'course_professor')
    prepopulated_fields = {"slug": ('course_code',)}
    class Meta:
        model = Course

admin.site.register(Course, CourseAdmin)



class StudentCourseAdmin(admin.ModelAdmin):
    
    class Meta:
        model = StudentCourse
        
        
admin.site.register(StudentCourse, StudentCourseAdmin)


class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'path', 'course')
    
    class Meta:

        model = Syllabus
        
        
admin.site.register(Syllabus, SyllabusAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    
    
    class Meta:

        model = Assignment
        
        
admin.site.register(Assignment, AssignmentAdmin)

class CourseNoteAdmin(admin.ModelAdmin):
    
    
    class Meta:

        model = CourseNote
        
        
admin.site.register(CourseNote, CourseNoteAdmin)
