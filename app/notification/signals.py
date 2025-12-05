from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from core.models import User, Course, Enrollment
from core.email_utils import EmailNotificationService


@receiver(post_save, sender=User)
def send_account_created_notification(sender, instance, created, **kwargs):
    """
    Send account creation notification when a new user is created.
    """
    if created:
        try:
            EmailNotificationService.send_account_created_notification(
                user=instance,
                password=None 
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send account creation notification for user {instance.email}: {str(e)}")


@receiver(pre_save, sender=Course)
def store_previous_teacher(sender, instance, **kwargs):
    """
    Store the previous teacher before saving to compare in post_save signal.
    """
    if instance.pk:
        try:
            old_instance = Course.objects.get(pk=instance.pk)
            instance._previous_teacher = old_instance.teacher
        except Course.DoesNotExist:
            instance._previous_teacher = None
    else:
        instance._previous_teacher = None


@receiver(post_save, sender=Course)
def send_course_assignment_notification(sender, instance, created, **kwargs):
    """
    Send course assignment notification when a teacher is assigned to a course.
    Uses the stored previous teacher for accurate comparison.
    """
    if instance.teacher:
        previous_teacher = getattr(instance, '_previous_teacher', None)
        
        if instance.teacher != previous_teacher:
            try:
                EmailNotificationService.send_course_assignment_notification(
                    teacher=instance.teacher,
                    course=instance
                )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send course assignment notification for course {instance.title}: {str(e)}")


@receiver(pre_save, sender=Enrollment)
def store_previous_enrollment_status(sender, instance, **kwargs):
    """
    Store the previous enrollment status before saving to compare in post_save signal.
    """
    if instance.pk:
        try:
            old_instance = Enrollment.objects.get(pk=instance.pk)
            instance._previous_status = old_instance.status
        except Enrollment.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Enrollment)
def handle_enrollment_notifications(sender, instance, created, **kwargs):
    """
    Handle both enrollment and removal notifications based on enrollment status changes.
    """
    if created and instance.status == 'ACTIVE':
        try:
            if instance.course.teacher:
                EmailNotificationService.send_enrollment_notification(
                    student=instance.student,
                    course=instance.course,
                    teacher=instance.course.teacher
                )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send enrollment notification for enrollment {instance.id}: {str(e)}")
    
    elif not created:
        previous_status = getattr(instance, '_previous_status', None)
        
        if previous_status == 'ACTIVE' and instance.status == 'DROPPED':
            try:
                if instance.course.teacher:
                    EmailNotificationService.send_removal_notification(
                        student=instance.student,
                        course=instance.course,
                        teacher=instance.course.teacher
                    )
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send removal notification for enrollment {instance.id}: {str(e)}")
