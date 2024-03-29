from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from .models import Product
from django.contrib import messages
from django.urls.base import reverse
from django.db.models.query_utils import Q
from products.models import Category
from django.db.models.functions.text import Lower
from products.forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin

# from django.template import context


class AllProducts(TemplateView):
    """
    A class show all products,
    including sorting and search queries
    """

    template_name = "products/products.html"

    def get(self, request):
        products = Product.objects.all()

        # Start as none to ensure we don't get an error
        # when loading the products page without a search term.
        query = None
        category = None
        sort = None
        direction = None

        # Access URL parameters by checking whether request.GET exists
        if request.GET:
            if "sort" in request.GET:
                sortkey = request.GET["sort"]
                sort = sortkey
                if sortkey == "name":
                    # annotate() allows us to add another field to the
                    # dataset returned from the database.
                    # Using the Lower() function on the original "name" field
                    products = products.annotate(lower_name=Lower("name"))
                    # The reason for copying the sort parameter
                    # into a new variable called sortkey,
                    # Is because now we've preserved the original field
                    # we want to sort on ("name").
                    # But we have the actual field we're going to sort on,
                    # ("lower_name") in the sort key variable.
                    # If we had just renamed sort itself to "lower_name"
                    # we would have lost the original field ("name")

                    # set the sortKey to lower_name
                    sortkey = "lower_name"

                if sortkey == "category":
                    sortkey = "category__name"

                if "direction" in request.GET:
                    direction = request.GET["direction"]
                    if direction == "desc":
                        # Add a minus in front of the sort key
                        # using string formatting, which reverses the order
                        sortkey = f"-{sortkey}"

                products = products.order_by(sortkey)

            if "category" in request.GET:
                # Split it into a list at the commas.
                categories = request.GET["category"].split(",")
                # Use that list to filter the current query set of all products
                # down to only products whose category name is in the list
                products = products.filter(category__name__in=categories)
                # Filter a list of Category objects
                # to those passed in the URL parameter
                category = Category.objects.filter(name__in=categories)

            # Since we named the text input in the form "q".
            # We can just check if "q" is in request.get
            if "q" in request.GET:
                # If "q" is a URL parameter
                # set it equal to a variable called query.
                query = request.GET["q"]
                # If the query is blank it's not going to return any results
                if not query:
                    # Use the Django messages framework
                    # to attach an error message to the request
                    messages.error(
                        request, "You didn't enter any search criteria"
                    )
                    # Redirect back to the products URL
                    return redirect(reverse("products"))

                # Django can't handle basic database OR logic
                # We want to return results where the query was matched
                # in either the product name OR the description
                # In order to accomplish this OR logic, we need to use Q
                # Set a variable equal to a Q object
                #  - Where the "name" contains the query
                #  - OR the "description" contains the query.
                # The pipe generates the OR statement.
                # The i in front of contains makes the queries case insensitive.
                queries = Q(name__icontains=query) | Q(
                    description__icontains=query
                )
                products = products.filter(queries)

        # If there is no sorting
        # The value of this variable will be the string "None_None".
        current_sorting = f"{sort}_{direction}"

        context = {
            "products": products,
            "search_term": query,
            "current_categories": category,
            "current_sorting": current_sorting,
        }

        return render(request, self.template_name, context)


class ProductDetail(TemplateView):
    """
    A view to show all individual product details
    """

    template_name = "products/product-details.html"

    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        context = {
            "product": product,
        }

        return render(request, self.template_name, context)


class AddProduct(LoginRequiredMixin, TemplateView):
    """
    A view to allow Admin users to add a product to the store
    """

    template_name = "products/add-product.html"

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, "Sorry, only store owners can do that")
            redirect(reverse("home"))

        form = ProductForm()
        context = {"form": form}

        return render(request, self.template_name, context)

    def post(self, request):
        # Instantiate a new instance of the ProductForm from request.POST and
        # include request .FILES also in order to make sure to capture
        # the image of the product if one was submitted
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product!")
            # Instead of redirecting to the addProduct page once the product is added,
            # redirect to that product''s detail page like the edit view does.
            # return redirect(reverse("addProduct"))
            return redirect(reverse("productDetails", args=[product.id]))
        else:
            # Attach a generic error message telling the user to check their form
            # which will display the errors.
            messages.error(
                request,
                "Failed to add product.  Please ensure the form is valid.",
            )
            context = {"form": form}

            return render(request, self.template_name, context)


class EditProduct(LoginRequiredMixin, TemplateView):
    """
    A view to allow Admin users to update a product in the store
    """

    # Tell the view which template to use.
    template_name = "products/edit-product.html"

    def get(self, request, product_id):
        if not request.user.is_superuser:
            messages.error(request, "Sorry, only store owners can do that")
            redirect(reverse("home"))

        # Prefill the form with the product details
        product = get_object_or_404(Product, pk=product_id)

        # Instantiate a ProductForm using the product
        form = ProductForm(instance=product)

        # Add an info message letting the user know that they're editing a product
        messages.info(request, f"You are editing {product.name}")

        # Give a context so the form and the product will be in the template
        context = {"form": form, "product": product}

        return render(request, self.template_name, context)

    def post(self, request, product_id):
        # Retrieve the amended product details
        product = get_object_or_404(Product, pk=product_id)

        # Instantiate a form using request.POST and request.FILES
        # Tell the form the specific instance we'd like to update is the product obtained above
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Successfully updated product!")
            return redirect(reverse("productDetails", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to update the product. Please ensure the form is valid.",
            )

            context = {"form": form, "product": product}

            return render(request, self.template_name, context)


class DeleteProduct(LoginRequiredMixin, TemplateView):
    """
    A view to allow Admin users to delete a product from the store
    Whenever someone makes a request to "products/delete/<some product id>"
    that product will be deleted.
    """

    # No template to use.
    template_name = ""

    def get(self, request, product_id):
        if not request.user.is_superuser:
            messages.error(request, "Sorry, only store owners can do that")
            redirect(reverse("home"))

        # Retrieve the product to be deleted
        product = get_object_or_404(Product, pk=product_id)
        product.delete()

        messages.success(request, f"Product {product.name} deleted")

        return redirect(reverse("products"))
