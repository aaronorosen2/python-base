echo "from django.contrib.auth import get_user_model; User = get_user_model();python3 from profile.models import UserProfile;from chat.models import Org,Channel,ChannelMember,Member;user=User.objects.create_superuser('admin01@gmail.com', 'admin01@gmail.com', '12345');userprofile=UserProfile.objects.update_or_create(user=user,);
Org.objects.create(user=User.objects.get(id=1), meta_attributes='KV');
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('admin02@gmail.com', 'admin02@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Org.objects.create(user=User.objects.get(id=2), meta_attributes='DPS');
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('bran@gmail.com', 'bran@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('sana@gmail.com', 'admin04@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('arya@gmail.com', 'admin04@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('rob@gmail.com', 'admin06@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('john@gmail.com', 'admin06@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile)
user=User.objects.create_superuser('jaime@gmail.com', 'admin06@gmail.com', '12345');
userprofile=UserProfile.objects.update_or_create(user = user,);
Member.objects.create(org=Org.objects.get(id=1),user=user,user_profile=userprofile);
Channel.objects.create(created_by=User.objects.get(id=1),name='class8',org=Org.objects.get(id=1));
Channel.objects.create(created_by=User.objects.get(id=2),name='class9',org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=1),added_by=User.objects.get(id=1),user=User.objects.get(id=1),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=1),added_by=User.objects.get(id=1),user=User.objects.get(id=2),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=1),added_by=User.objects.get(id=1),user=User.objects.get(id=3),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=1),added_by=User.objects.get(id=1),user=User.objects.get(id=4),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=2),added_by=User.objects.get(id=2),user=User.objects.get(id=1),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=2),added_by=User.objects.get(id=2),user=User.objects.get(id=2),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=2),added_by=User.objects.get(id=2),user=User.objects.get(id=5),org=Org.objects.get(id=1));
ChannelMember.objects.create(Channel=Channel.objects.get(id=2),added_by=User.objects.get(id=2),user=User.objects.get(id=6),org=Org.objects.get(id=1));" | python manage.py shell


user_profile

echo "from django.contrib.auth import get_user_model;from profile.models import UserProfile; User = get_user_model();  user = User.objects.create_user('aime@gmail.com', 'aime@gmail.com', '12345');UserProfile.objects.update_or_create(user = user,);" | python manage.py shell

user and super_user
echo "from django.contrib.auth import get_user_model;User.objects.create_user('sanjay@gmail.com', 'sanjay06@gmail.com', '12345');User.objects.create_user('anmol@gmail.com', 'anmol@gmail.com', '12345');User.objects.create_user('nayan@gmail.com', 'nayan@gmail.com', '12345');User.objects.create_user('yogita@gmail.com', 'yogita@gmail.com', '12345');" | python manage.py shell



Channel :-
echo "from django.contrib.auth import get_user_model;User=get_user_model();from chat.models import Channel,Org;print(Org.objects.get(id=1));Channel.objects.create(created_by=User.objects.get(id=1),name='class9',org=Org.objects.get(id=1));Channel.objects.create(created_by=User.objects.get(id=3),name='class8',org=Org.objects.get(id=1));"| python3 manage.py shell


Member:-
echo "from django.contrib.auth import get_user_model;User=get_user_model();from chat.models import Member,Org;Member.objects.create(user=User.objects.get(id=1),org=Org.objects.get(id=1));Member.objects.create(user=User.objects.get(id=2),org=Org.objects.get(id=2));"| python3 manage.py shell



channel Member:-
echo "from django.contrib.auth import get_user_model;User=get_user_model();from chat.models import ChannelMember,Channel,Org;ChannelMember.objects.create(Channel=Channel.objects.get(id=3),added_by=User.objects.get(id=3),user=User.objects.get(id=4),org=Org.objects.get(id=2));ChannelMember.objects.create(Channel=Channel.objects.get(id=4),added_by=User.objects.get(id=3),user=User.objects.get(id=3),org=Org.objects.get(id=3));ChannelMember.objects.create(Channel=Channel.objects.get(id=3),added_by=User.objects.get(id=6),user=User.objects.get(id=3),org=Org.objects.get(id=2));"| python3 manage.py shell


org:-
echo "from django.contrib.auth import get_user_model;User=get_user_model();from chat.models import Org;Org.objects.create(user=User.objects.get(id=1), meta_attributes='KV') Org.objects.create(user=User.objects.get(id=2), meta_attributes='Vikram')" | python3 manage.py shell