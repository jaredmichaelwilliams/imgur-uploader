imgur-uploader
==============

A simple command line client for uploading files to Imgur.

Created for my `PyCon US 2015 Docker tutorial
<https://us.pycon.org/2015/schedule/presentation/312/>`_ so that students using
my cloud servers can see the gifs they create at the end of exercise 1.

This tool is open source under the `MIT License <LICENSE>`_.

Quickstart
----------

Getting Imgur API credentials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to https://api.imgur.com/oauth2/addclient and register a new Imgur API
client. You will need an Imgur account to do this.

You can put it any valid URL for the callback URL - we won't be using it.

Installing imgur-uploader
^^^^^^^^^^^^^^^^^^^^^^^^^

Installing imgur-uploader is easy. It runs on versions of Python >=2.7 or >=3.3.

If you just want to use imgur-uploader, you can just ``pip install
imgur-uploader``.

If you want to tweak or enhance imgur-uploader, follow these instructions:

#. Clone this repository
#. Install the tool with ``pip install -e .``

Using imgur-uploader
^^^^^^^^^^^^^^^^^^^^


``Options:``

``--image PATH``

``--login        Login To Imgur``

``--add-details  Add a title and Description``

``--help         Show this message and exit.``


First, create a file called ``~/.config/imgur_uploader/uploader.cfg``, with the
following contents (substitute your credentials)::

    [imgur]
    id = 9354da9ecdcfae3
    secret = 8387eca75687ecad9876ead47786edac0875dc0d

(Optional) Login to imgur by running ``imgur-uploader --login``
it will provide a link to go to:

    Please Go To https://api.imgur.com/oauth2/authorize?client_id=5331f47b697084b&response_type=pin
    Please enter pin from the imgur login:

Go to the link in your browser and copy the provided pin.
it will add the ``access_token`` and ``refresh_token`` to ``~/.config/imgur_uploader/uploader.cfg``

If you wish to upload files anonymously dont run the login command

Upload an image by running ``imgur-uploader --image path/to/my.gif``

If you want to add a title and description run ``imgur-uploader --image path/to/my.gif --add-details``
you will then be prompted to enter a title and description

The tool will return a shortened link to your uploaded gif upon completion::

    Uploading file my.gif
    ...
    File uploaded - see your gif at http://i.imgur.com/6WsQPpw.gif
