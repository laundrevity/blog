WIP, <a href="https://github.com/laundrevity/xparse">repo is here</a>

<h2>Understanding Data Serialization with Rust and Python: A Deep Dive into Memory Layout and XML-Specified Message Formats</h2>

<h3>Introduction</h3>
In the realm of software development, efficient data serialization – the process of converting data structures into a format that can be easily stored or transmitted – is crucial. Our project aims to simplify this process by providing a robust tool that generates Rust code and Python bindings. This tool focuses on serializing and deserializing specific message formats, as defined in XML schemas.

At its heart, this project leverages the power and safety of Rust, coupled with the versatility of Python, to handle complex data serialization tasks. By defining message formats in XML, users can specify the structure of data that needs to be serialized or deserialized, leading to a highly customizable and scalable solution.

<h3>XML in message formatting</h3>

XML plays a pivotal role in our system. It allows users to define message formats in a clear, hierarchical manner. For instance, consider the following snippet from `school.xml`:

```xml
<messageFormat id="1" name="person">
    <attribute name="id" type="int" length="4" required="true"/>
    ...
</messageFormat>
```

Here, each message format, like person, is detailed with attributes such as id, name, age, specifying their data types and lengths

<h3>Message structure in memory</h3>

<img src="/static/tikz/header_body.png" alt="Memory Layout" width="50%">

Figure 1: The memory layout of a serialized message, highlighting the header and data sections.

As shown in Figure 1, each message begins with a header. The header consists of:

- 4-byte message length, indicating the total length of the message (including the header)
- 1-byte message type, specifying the format of the message, correlating to the `id` in the XML schema
- 4-byte bitmask, a binary mask specifying which optional fields are present in the message.

Following the header is the data section, which contains the serialized attributes as defined in the XML. For example, if the XML specification of our message is 
```xml
<messageFormat id="2" name="position">
    <attribute name="quantity" type="int" length="8" required="true"/>
    <attribute name="account_id" type="uint" length="4" required="false"/>
    <attribute name="instrument_id" type="uint" length="8" required="true"/>
    <attribute name="symbol" type="str" length="20" required="false"/>
</messageFormat>
```
then the data section would look like 

<img src="/static/tikz/diagram.png" alt="Data Section Layout" width="50%">

for a message including the optional `account_id` attribute.
