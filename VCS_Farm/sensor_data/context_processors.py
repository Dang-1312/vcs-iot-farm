from .models import NutrientAlert

def nutrient_alert(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return {'nutrient_alert': "Đăng nhập để xem!"}
    alert = None
    latest_alert = NutrientAlert.objects.latest('timestamp')
    print(f"DEBUG - Latest alert: {latest_alert}")
    if latest_alert and latest_alert.error_message.lower() == "warning":
        alert = "Hết chất dinh dưỡng!"
    return {'nutrient_alert': alert}