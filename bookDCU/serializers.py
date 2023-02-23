'''Provisional implementation of serializers for the API. Serializers are used to convert data to and from JSON format.'''
'''Potential for future development with Django REST Framework and Node.js'''

# from rest_framework import serializers
# from .models import *

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = APIUser
#         fields = ['username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         email = validated_data['email']
#         username = validated_data['username']
#         password = validated_data['password']

#         new_user = APIUser.objects.create_user(email=email, username=username, password=password)
#         new_user.save()
#         return new_user

# # was HyperlinkedModelSerializer but changed to ModelSerializer
# class RoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Room
#         fields = ['id', 'building', 'capacity', 'seatmap_image', 'campus', 'campus_choice']

# class BasketItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BasketItem
#         fields = ['id', 'date_created', 'basket_id', 'name', 'room_id', 'start_time', 'end_time', 'seat_number', 'is_active']

# class AddBasketItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BasketItem
#         fields = ['room_id', 'start_time', 'end_time', 'seat_number']

#     def create(self, validated_data):
#         room_id = validated_data['room_id']
#         start_time = validated_data['start_time']
#         end_time = validated_data['end_time']
#         seat_number = validated_data['seat_number']

#         request = self.context.get('request', None)

#         if request:
#             current_user = request.user
#             basket = Basket.objects.filter(user_id=current_user, is_active=True).first()
#             if basket is None:
#                 basket = Basket.objects.create(user_id=current_user)
            
#             basket_items = BasketItem.objects.filter(room_id=room_id, basket_id=basket, start_time=start_time, end_time=end_time, seat_number=seat_number).first()
#             if basket_items:
#                 pass
#             else:
#                 new_basket_item = BasketItem.objects.create(basket_id=basket, room_id=room_id, start_time=start_time, end_time=end_time, seat_number=seat_number)
#                 return new_basket_item
#         else:
#             return None

# class RemoveBasketItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BasketItem
#         fields = ['room_id', 'start_time', 'end_time', 'seat_number']

#     def create(self, validated_data):
#         room_id = validated_data['room_id']
#         start_time = validated_data['start_time']
#         end_time = validated_data['end_time']
#         seat_number = validated_data['seat_number']
        
#         request = self.context.get('request', None)
#         if request:
#             current_user = request.user
#             basket = Basket.objects.filter(user_id=current_user, is_active=True).first()
#             # Check if the item is already in the basket
#             basket_items = BasketItem.objects.filter(room_id=room_id, basket_id=basket, start_time=start_time, end_time=end_time, seat_number=seat_number).first()
#             if basket_items:
#                 basket_items.delete()
#                 return BasketItem(room_id=room_id, basket_id=basket, start_time=start_time, end_time=end_time, seat_number=seat_number)
#             else:
#                 return BasketItem(room_id=room_id, basket_id=basket, start_time=start_time, end_time=end_time, seat_number=seat_number)
#         else:
#             return None

# class BasketSerializer(serializers.ModelSerializer):
#     items = BasketItemSerializer(many=True, read_only=True, source='basketitem_set')
#     class Meta:
#         model = Basket
#         fields = ['id', 'user_id', 'is_active', 'date_created', 'items']

# # was HyperlinkedModelSerializer
# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['id', 'date_booked', 'basket_id', 'user_id', 'name', 'room_id', 'start_time', 'end_time', 'seat_number', 'is_active']

# class SeatSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Seat
#         fields = ['id', 'room_id', 'seat_number', 'is_booked', 'date_created']

# class APIUserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = APIUser
#         fields = ['id', 'email', 'username']

# class CheckoutSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['basket_id', 'room_id']

#     def create(self, validated_data):
#         request = self.context.get('request', None)
#         current_user = request.user
#         basket_id = validated_data['basket_id']

#         # NEED TO SPECIFY ROOM ID FOR NOW, NEED TO CHANGE THIS
#         room_id = validated_data['room_id']
#         print(basket_id)
#         # name = validated_data['name']

#         basket_id.is_active = False
#         basket_id.save()

#         booking = Booking.objects.create(basket_id=basket_id, user_id=current_user, room_id=room_id)

#         new_basket = Basket.objects.create(user_id=current_user)
        
#         return booking
