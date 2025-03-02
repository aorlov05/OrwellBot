Object subclass: MessageDetector [
    | message |
    <comment: 'Represents an object which filters messages into categories.'>
    MessageDetector class >> new: aMessage [
        <category: 'create message detector object'>
        | create |
        create := super new.
        create init: aMessage ifNil: [''].
        ^create
    ]
    init: aMessage ifNil: aDefault [
        <category: 'initialization with a passed in message, default to empty string'>
        " message := aMessage ifNil: [aDefault]. "
        message := (aMessage ifNil: [aDefault]) asString.
    ]
    showMessage [
        <category: 'prints the message to console'>
        Transcript show: message; nl.
    ]
    isHttp [
        <category: 'checks if a link starts with http://, https://, or www.'>
        | prefixes isMatch |
        prefixes := Array with: 'http://' with: 'https://' with: 'www.'.
        isMatch := false.

        prefixes do: [:prefix |
            (message copyFrom: 1 to: prefix size) = prefix ifTrue: [
                isMatch := true.
                Transcript show: 'True: ', prefix; nl.
                ^isMatch.
            ].
        ].

        isMatch ifFalse: [
            Transcript show: 'False'; nl.
        ].
    ]
]
