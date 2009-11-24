#ifndef CVE2009_3300
#define CVE2009_3300

namespace shibsp {
    void HTTPResponse_setResponseHeader(const char* name, const char* value);
    long HTTPResponse_sendRedirect(const char* url);
}

#endif
