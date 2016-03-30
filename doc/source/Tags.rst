Define required tags
====================

**Tag resolution**

It is possible to specify tags in the config file by name and by xml path.

1. By name: only 'tagname'
2. By XML path: <parentTag><oneChildTag><DesiredTag>?§$%-*"!?</...></...></...>

1.
    If you use the tagname version you should be aware of behavior since this method checks
    all existing tags regardless of their positions in the XML tree. So if there are multiple tags
    with the same name they all need to pass the test to get positive validation result.

2.
    If you use a path to specify you would only target all tags which match to the given path. The path is relative
    to the root element of the meta data XML (In the case of SDE meta data this is the <metadata> tag). Thus this tag
    may not be part of your path

**Rules**

Default tags::

    <tag>Here comes some content</tag>

    "tag_config" : {
        "required" : [
          {
            "tag_name" : "tag",
            "mapped_name" : "desiredName in emails",
          }
        ]
      }

This means for the validation:

- Tag with the defined name must exist in the XML
- Tag is automatically not_empty --> content between tags necessary <tag>content</tag>
-
    Attributes can be defined additionally. If a configuration for attributes exist the tag
    must contain them and the attributes must be populated with values

Empty tags::

    <tag attributeName="attributeValue"/>

    "tag_config" : {
        "required" : [
          {
            "tag_name" : "parentTag/childTag/tag",
            "is_empty" : true,
            "attributes" : ["attriubteName", ... ]
            "mapped_name" : "desiredName in emails",
          }
        ]
      }

This means for the validation:

- Tag name must exists

-
    Is_empty specifies that an empty tag <tag /> is allowed. It is mandatory to mark empty tags with
    is_empty since without this marker the tag would be treated as not empty tag and must have content.
    Thus the validation would fail.

-
    If attributes are defined <tag attr="value" /> they must exist else
    the tag is also valid without attributes <tag/>

-
    It is recommended to use qualified paths to identify tags
    else undesired behavior is possible because of equally named tags in the XML (See tag resolution)