# Sphinx (reStructuredText) Reference Guide

## 1. Document Structure and Basics

* **Indentation:** Use a consistent indentation of 3 spaces for reST files.
* **Line Length:** Limit normal text to 80 characters, though tables and long links may exceed this.
* **Paragraphs:** Separate paragraphs with one or more blank lines. All lines in a paragraph must share the same left alignment.
* **Lists:** Use an asterisk `*` for bulleted lists and `1.` or `#.` for numbered lists. Nested lists must be separated from parent items by blank lines.
* **Sections:** Create headers by underlining the title with punctuation (e.g., `=` for sections, `-` for subsections) at least as long as the text.

## 2. Inline Markup

* **Emphasis:** Use one asterisk `*text*` for italics.
* **Strong Emphasis:** Use two asterisks `**text**` for boldface.
* **Code/Literals:** Use double backquotes ```text``` for code samples, variables, and literals.
* **Arguments:** Use single asterisks `*arg*` for function and method arguments.
* **Standard Values:** Use code markup for `True`, `False`, and `None`.
* **Hyperlinks:** Use ``Link text <URL>`__` for inline web links, preferring anonymous links (double underscore).

## 3. Directives

Directives are explicit markup blocks starting with `.. name::`.

### 3.1 Information Units (Objects)

* **Module:** `.. module:: name` identifies the module; use options like `:platform:` and `:synopsis:`.
* **Function:** `.. function:: name(params)` describes module-level functions.
* **Class:** `.. class:: Name(params)` describes a class and its constructor arguments.
* **Method:** `.. method:: name(params)` describes an object method; do not include the `self` parameter.
* **Attribute:** `.. attribute:: name` describes an object data attribute.

### 3.2 Admonitions and Metadata

* **Notes:** `.. note::` provides especially important information about an API.
* **Warnings:** `.. warning::` highlights critical info regarding crashes, data loss, or security.
* **Version Control:**
    * `.. versionadded:: version` identifies when a feature was introduced.
    * `.. versionchanged:: version` describes changes to an existing feature and must include an explanation.
    * `.. deprecated:: version` indicates when a feature was deprecated.

## 4. Cross-Referencing Roles

Roles use the syntax `:rolename:`content``.

* **Python Objects:** Use `:mod:` (module), `:func:` (function), `:class:` (class), `:meth:` (method), and `:attr:` (attribute).
* **Display Modifiers:**
    * `:role:`title <target>``: Displays "title" instead of the target name.
    * `:role:`~target``: Displays only the last component of the target (e.g., `get` instead of `Queue.get`).
    * `:role:`!target``: Formats the text without creating a hyperlink.
* **References:** Use `:pep:` for PEPs, `:rfc:` for RFCs, and `:term:` for glossary terms.
* **Internal Links:** Use `:ref:`label-name`` to reference a unique label defined via `.. _label-name:`.

---

## 5. Code Examples

* **Literal Blocks:** Introduce blocks by ending a paragraph with `::` and indenting the code.
* **Interactive Sessions:** Include Python prompts (`>>>`) and output directly; they are recognized automatically.
* **Code-Block:** Use `.. code-block:: language` to specify the highlighting for a single block.
* **External Files:** Use `.. literalinclude:: filename` to include source files as verbatim text.

---

## 6. Example Usage

```rst
.. function:: send_message(recipient, body, priority=0)

   Sends an encrypted message to the recipient.

   :param recipient: The ID of the message receiver.
   :type recipient: str

   .. versionadded:: 3.14
      Support for priority levels.

   .. note::
      Messages are stored for 30 days.

   See :func:`~myapp.utils.validate_id` for validation details.

```
