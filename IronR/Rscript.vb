Imports Microsoft.Scripting.Hosting

Public Module Rscript

    ReadOnly eng As ScriptEngine = IronPython.Hosting.Python.CreateEngine()
    ReadOnly scope As ScriptScope = eng.CreateScope()

    Sub New()
        eng.Execute("
            def greetings(name):
                return 'Hello ' + name.title() + '!'
            ", scope)

        Dim greetings As Func(Of String, String) = scope.GetVariable("greetings")
        Console.WriteLine(greetings("world"))
    End Sub
End Module
