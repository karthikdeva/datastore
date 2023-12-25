# # import graphene
# # import graphql_jwt
# import django_filters
# import datetime as dt
# from functools import reduce
# # from graphql_jwt.decorators import login_required, permission_required
# from django.contrib.auth.models import User  # Import the User model

# from django.contrib.auth.mixins import LoginRequiredMixin
# # from graphene_django.filter import DjangoFilterConnectionField
# from .models import Citizen

# from .model_input import CitizenInput
# from .model_node import CitizenNode,  UserNode


# def change_case(str):
#     return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, str).lower()


# # class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
# #     user = graphene.Field(UserNode)

# #     @classmethod
# #     def resolve(cls, root, info, **kwargs):
# #         return cls(user=info.context.user)


# class CitizenFilter(django_filters.FilterSet):
#     # Do case-insensitive lookups on 'name'
#     name = django_filters.CharFilter(lookup_expr=['exact', 'icontains', 'istartswith'])

#     class Meta:
#         abstract = True
#         fields = ['name']


# # class Query(graphene.ObjectType):
# #     me = graphene.Field(UserNode)
# #     citizen = DjangoFilterConnectionField(CitizenNode)


# #     @staticmethod
# #     @login_required
# #     def resolve_me(self, info):
# #         user = info.context.user
# #         return user

# #     @staticmethod
# #     @login_required
# #     def resolve_citizen(root, info, **kwargs):
# #         #status
# #         return Citizen.objects.all()

# ###
# # Citizen starts here
# ###

# class CreateCitizen(graphene.Mutation):
#     class Arguments:
#         citizen_data = CitizenInput(required=True)
#     citizen = graphene.Field(CitizenNode)

#     @staticmethod
#     @login_required
#     def mutate(root, info, citizen_data=None):
#         user_id = info.context.user.id
#         user = User.objects.get(id=user_id)
#         citizen = Citizen(
#             timestamp=citizen_data.timestamp,
#             name = citizen_data.name,
#             email = citizen_data.email,
#             address = citizen_data.address,
#             phone = citizen_data.phone,
#             adhar = citizen_data.adhar,
#             epic = citizen_data.epic,
#             no_response = citizen_data.no_response,
#         )
#         citizen.save()
#         return CreateCitizen(citizen)


# class UpdateCitizen(graphene.Mutation):
#     class Arguments:
#         citizen_data = CitizenInput(required=True)

#     citizen = graphene.Field(CitizenNode)

#     @staticmethod
#     @login_required
#     def mutate(root, info, citizen_data=None):
#         citizen = Citizen.objects.get(code=citizen_data.id)
#         citizen_data.pop('id')
#         citizen_data['modified_at'] = dt.datetime.now()
#         citizen_data['updated_by'] = User.id
#         if citizen is not None:

#             for key, value in citizen_data.items():
#                 key = change_case(key)
#                 setattr(citizen, key, value)
#             citizen.save()

#         return UpdateCitizen(citizen)


# class DeleteCitizen(graphene.Mutation):
#     class Arguments:
#         id = graphene.String()
#     citizen = graphene.Field(CitizenNode)

#     @staticmethod
#     @login_required
#     def mutate(root, info, id):
#         citizen = Citizen.objects.get(code=id)
#         if citizen is not None:
#             # citizen.status = True
#             citizen.modified_at = dt.datetime.now()
#             citizen.save()
#         return DeleteCitizen(citizen)


# class Mutation(graphene.ObjectType):
#     token_auth = ObtainJSONWebToken.Field()
#     verify_token = graphql_jwt.Verify.Field()
#     refresh_token = graphql_jwt.Refresh.Field()

#     create_citizen = CreateCitizen.Field()
#     update_citizen = UpdateCitizen.Field()
#     delete_citizen = DeleteCitizen.Field()


# schema = graphene.Schema(query=Query, mutation=Mutation)
