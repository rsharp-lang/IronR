Imports IronPython.Runtime
Imports Microsoft.Scripting.Hosting

Module Program

    ReadOnly eng As ScriptEngine = IronPython.Hosting.Python.CreateEngine()
    ReadOnly scope As ScriptScope = eng.CreateScope()

    Sub Main()
        eng.Execute("
def greetings(name):
    return 'Hello ' + name.title() + '!'
", scope)

        Dim greetings = scope.GetVariable("greetings")

        Console.WriteLine(greetings("world"))
        Pause()
    End Sub

End Module
