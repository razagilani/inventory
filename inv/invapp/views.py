from django.shortcuts import get_object_or_404, render_to_response

from invapp.models import Collection, Project, Item, Bag, BagAction


def collection(request, id):
    collection = get_object_or_404(Collection, id=id)
    projects = Project.objects.filter(collection=collection).defer('collection',
        'created')
    items = Item.objects.defer('created', 'original_item_type', 'rawfiles_loc',
        'qcfiles_loc', 'qafiles_loc', 'finfiles_loc', 'ocrfiles_loc',
        'notes').filter(collection=collection)
    return render_to_response('collection.html',
        {'collection': collection, 'projects': projects, 'items': items})


def project(request, id):
    project = get_object_or_404(Project, id=id)
    items = Item.objects.defer('collection', 'created', 'original_item_type',
        'rawfiles_loc', 'qcfiles_loc', 'qafiles_loc', 'finfiles_loc',
        'ocrfiles_loc', 'notes').filter(project=project)
    return render_to_response('project.html',
        {'project': project, 'items': items})


def item(request, id):
    item = get_object_or_404(Item, id=id)
    bags = Bag.objects.defer('created', 'bag_type', 'payload_raw').filter(item=item)
    return render_to_response('item.html', {'item': item, 'bags': bags})


def bag(request, bagname):
    bag = get_object_or_404(Bag, bagname=bagname)
    actions = BagAction.objects.filter(bag=bag)
    return render_to_response('bag.html', {'bag': bag, 'actions': actions})

def home(request):
    collections = Collection.objects.all()
    projects = Project.objects.all()
    items = Item.objects.order_by('created').reverse()[:20]
    return render_to_response('home.html', {'collections': collections,
        'projects': projects, 'items': items})
