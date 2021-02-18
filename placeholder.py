
import sys
import os
from django.conf import settings

from django.http import HttpResponse, HttpResponseBadRequest

from django.conf.urls import url

from django.core.wsgi import get_wsgi_application



# settings configurations
DEBUG = os.environ.get("DEBUG", 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'fi(7+o0_d231#m$@uw2d68s_s$6dag-g)62wxjc%ve5e23s&0u')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

settings.configure(
	DEBUG=DEBUG,
	SECRET_KEY=SECRET_KEY,
	ALLOWED_HOSTS=ALLOWED_HOSTS,
	ROOT_URLCONF=__name__,
	MIDDLEWARE_CLASSES=(
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
	),
)


from django import forms
from io import BytesIO
from PIL import Image, ImageDraw

class ImageForm(forms.Form):
	"""Form to validate requested placeholder image."""
	height = forms.IntegerField(min_value=1, max_value=2000)
	width = forms.IntegerField(min_value=1, max_value=2000)

	def generate(self, image_format="PNG"):
		"""Generate an image of the given type and return as raw bytes."""
		height = self.cleaned_data['height']
		width = self.cleaned_data['width']
		image = Image.new('RGB', (width, height))
		draw = ImageDraw.Draw(image)
		text = '{} X {}'.format(width, height)
		textwidth, textheight = draw.textsize(text)
		if textwidth < width and textheight < height:
			texttop = (height - textheight) // 2
			textleft = (width - textwidth) // 2
			draw.text((textleft, texttop), text, fill=(255, 255, 255))
		content = BytesIO()
		image.save(content, image_format)
		content.seek(0)
		return content


def placeholder(request, width, height):
	form = ImageForm({'height': height, 'width': width})
	if form.is_valid():
		image = form.generate()
		# height = form.cleaned_data['height']
		# width = form.cleaned_data['width']
		return HttpResponse(image, content_type='image/png')
	# TODO: Rest of the view will go here
	#para = "The width" + width + " Hieght:" + height
	else:
		return HttpResponseBadRequest("Invalid image request")


def index(request):

	return HttpResponse('Hello World')

urlpatterns = (
	url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
	url(r'^$', index),
)
# wsgi application
application = get_wsgi_application()
if __name__ == "__main__":
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)




