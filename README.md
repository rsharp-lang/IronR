# IronR

interop package for R calling functions from R# library based on the ``Rcpp/.NetCore host cpp`` solution.
this solution is targetted .NETCore 5 and used for build a Rcpp package. 

## .NetCore and C++

+ (Write a custom .NET Core host to control the .NET runtime from your native code)[https://docs.microsoft.com/en-us/dotnet/core/tutorials/netcore-hosting]

for .netcore5 runtime, use ``hostfxr`` library:

Step 1 - Load hostfxr and get exported hosting functions

```cpp
// Using the nethost library, discover the location of hostfxr and get exports
bool load_hostfxr()
{
    // Pre-allocate a large buffer for the path to hostfxr
    char_t buffer[MAX_PATH];
    size_t buffer_size = sizeof(buffer) / sizeof(char_t);
    int rc = get_hostfxr_path(buffer, &buffer_size, nullptr);
    if (rc != 0)
        return false;

    // Load hostfxr and get desired exports
    void *lib = load_library(buffer);
    init_fptr = (hostfxr_initialize_for_runtime_config_fn)get_export(lib, "hostfxr_initialize_for_runtime_config");
    get_delegate_fptr = (hostfxr_get_runtime_delegate_fn)get_export(lib, "hostfxr_get_runtime_delegate");
    close_fptr = (hostfxr_close_fn)get_export(lib, "hostfxr_close");

    return (init_fptr && get_delegate_fptr && close_fptr);
}
```

Step 2 - Initialize and start the .NET Core runtime

```cpp
// Load and initialize .NET Core and get desired function pointer for scenario
load_assembly_and_get_function_pointer_fn get_dotnet_load_assembly(const char_t *config_path)
{
    // Load .NET Core
    void *load_assembly_and_get_function_pointer = nullptr;
    hostfxr_handle cxt = nullptr;
    int rc = init_fptr(config_path, nullptr, &cxt);
    if (rc != 0 || cxt == nullptr)
    {
        std::cerr << "Init failed: " << std::hex << std::showbase << rc << std::endl;
        close_fptr(cxt);
        return nullptr;
    }

    // Get the load assembly function pointer
    rc = get_delegate_fptr(
        cxt,
        hdt_load_assembly_and_get_function_pointer,
        &load_assembly_and_get_function_pointer);
    if (rc != 0 || load_assembly_and_get_function_pointer == nullptr)
        std::cerr << "Get delegate failed: " << std::hex << std::showbase << rc << std::endl;

    close_fptr(cxt);
    return (load_assembly_and_get_function_pointer_fn)load_assembly_and_get_function_pointer;
}
```

Step 3 - Load managed assembly and get function pointer to a managed method

```cpp
// Function pointer to managed delegate
component_entry_point_fn hello = nullptr;
int rc = load_assembly_and_get_function_pointer(
    dotnetlib_path.c_str(),
    dotnet_type,
    dotnet_type_method,
    nullptr /*delegate_type_name*/,
    nullptr,
    (void**)&hello);
```

```vbnet
Public Delegate Function ComponentEntryPoint(args As IntPtr, sizeBytes As Integer) As Integer
```

Step 4 - Run managed code!

```cpp
lib_args args
{
    STR("from host!"),
    i
};

hello(&args, sizeof(args));
```

## Rcpp and C++

+ Rcpp: Seamless R and C++ Integration

R package ``NAMESPACE`` file

```R
useDynLib(IronR)
exportPattern("^[[:alpha:]]+")
importFrom(Rcpp, evalCpp)
```

custom attributes in cpp source file for export api function to R language

```cpp
//[[Rcpp::interfaces(r, cpp)]]
```