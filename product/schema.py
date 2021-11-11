from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from .models import *


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)


    def resolve_categories(root, info, **kwargs):
        return Category.objects.all()




class CreateCategory(graphene.Mutation):
    class Arguments:
        # Mutation to create a category
        title = graphene.String(required=True)

    # Class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title):
        category = Category()
        category.title = title
        category.save()
        
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        id = graphene.ID()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, title, id):
        category = Category.objects.get(pk=id)
        category.title = title
        category.save()

        return UpdateCategory(category=category)


class Mutation(graphene.ObjectType):
    update_category = UpdateCategory.Field()
    create_category = CreateCategory.Field()


schema = graphene.Schema(query= Query, mutation=Mutation)