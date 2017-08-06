==============
 Contributing
==============

While Ergonomica aims to, by being open source, be a project for and maintained by the community, there are a few rules that should be generally followed. This file outlines those guidelines as well as how the GitHub contribution process works.

Pull Request Process
====================

If you are confused about how to do the following tasks, they're written up much more nicely in GitHub's documentation; I suggest you search that.

1. Create a fork of :code:`ergonomica/ergonomica`, typically under your account.
2. Make your desired changes.
3. Add unit tests in the :code:`tests` directory for testing changes. This both helps ensure your new code is stable and makes you, in the process of writing tests, consider *how* you want the feature to work.
3. Create a pull request detailing *what* is changed and *why* this change is necessary/improves users' experience. Additionally, include some documentation on how to use this command.
4. This pull request will be automatically tested against the Ergonomica CI (including your additional tests). If it doesn't pass, revise your changes until it does.
5. If approved, your pull request will be merged into :code:`master`!

These steps are just an outline of the process; feel free to submit unfinished pull requests and we'll help with the rest!
